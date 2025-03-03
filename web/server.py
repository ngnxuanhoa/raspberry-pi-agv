"""Web server for AGV control interface"""
from flask import Flask, render_template, Response, jsonify, request
from functools import wraps
import cv2
import numpy as np
import socket
from config import WEB_HOST, WEB_PORT, WEB_USERNAME, WEB_PASSWORD

app = Flask(__name__)

# Global references to be set from main
camera = None
slam = None
path_planner = None

def get_local_ip():
    """Get local IP address"""
    try:
        # Get local IP by creating a dummy connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return 'localhost'

def check_auth(username, password):
    """Check if username/password combination is valid"""
    print(f"Auth attempt - Username: {username}")  # Debug log
    is_valid = username == WEB_USERNAME and password == WEB_PASSWORD
    print(f"Auth result: {'success' if is_valid else 'failed'}")  # Debug log
    return is_valid

def authenticate():
    """Send 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            print("Authentication failed or no credentials provided")  # Debug log
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def gen_frames():
    """Video streaming generator function"""
    while True:
        if camera:
            frame = camera.get_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
@requires_auth
def index():
    """Serve the main page"""
    print("Serving index page")  # Debug log
    local_ip = get_local_ip()
    return render_template('index.html', local_ip=local_ip)

@app.route('/video_feed')
@requires_auth
def video_feed():
    """Video streaming route"""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/map')
@requires_auth
def get_map():
    """Get current SLAM map"""
    if slam:
        map_data = slam.get_map()
        ret, buffer = cv2.imencode('.jpg', map_data)
        response = buffer.tobytes()
        return Response(response, mimetype='image/jpeg')
    return ''

@app.route('/set_target', methods=['POST'])
@requires_auth
def set_target():
    """Set new target position"""
    data = request.get_json()
    if path_planner and 'x' in data and 'y' in data:
        path_planner.set_target((data['x'], data['y']))
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})

def start_server():
    """Start the web server"""
    local_ip = get_local_ip()
    print(f"\nAGV Web Interface available at:")
    print(f"http://{local_ip}:{WEB_PORT}")
    print(f"Username: {WEB_USERNAME}")
    print(f"Password: {WEB_PASSWORD}\n")
    app.run(host=WEB_HOST, port=WEB_PORT)