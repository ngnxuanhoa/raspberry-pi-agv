let mapCanvas = document.getElementById('mapCanvas');
let ctx = mapCanvas.getContext('2d');
let statusText = document.getElementById('statusText');
let positionText = document.getElementById('positionText');
let stopBtn = document.getElementById('stopBtn');

// Map click handling
mapCanvas.addEventListener('click', function(event) {
    const rect = mapCanvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    // Send target position to server
    fetch('/set_target', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            x: x,
            y: y
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            statusText.textContent = 'Moving to target';
            drawTarget(x, y);
        }
    });
});

// Emergency stop
stopBtn.addEventListener('click', function() {
    fetch('/stop', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        statusText.textContent = 'Stopped';
    });
});

// Update map
function updateMap() {
    fetch('/map')
    .then(response => response.blob())
    .then(blob => {
        const img = new Image();
        img.onload = function() {
            ctx.drawImage(img, 0, 0, mapCanvas.width, mapCanvas.height);
        };
        img.src = URL.createObjectURL(blob);
    });
}

function drawTarget(x, y) {
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
}

// Update map periodically
setInterval(updateMap, 1000);
