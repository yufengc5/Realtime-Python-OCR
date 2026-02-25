// Camera setup function - returns a Promise so we have to call it in an async function
async function setupCamera() {
    // Find the video element on our HTML page
    video = document.getElementById('video');
    
    // Request the rear camera of the device
    const stream = await navigator.mediaDevices.getUserMedia({
        'audio': false,
        'video': {
          facingMode: { ideal: "environment" },
          width: { ideal: 960 },
          height: { ideal: 960},
      }});
    video.srcObject = stream;
    
    // Handle the video stream once it loads.
    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

function drawWebcamContinuous(){
    ctx.drawImage(video,0,0);
    requestAnimationFrame(drawWebcamContinuous);
}

var canvas;
var ctx;

async function main() {
    // set up camera
    await setupCamera();
    video.play()

    // set up canvas 
    canvas = document.getElementById('cameracanvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx = canvas.getContext('2d');
  
    // start continuous drawing function
    drawWebcamContinuous();
  
    console.log("Camera setup done")
}

// Run the main function once the page is fully loaded
document.addEventListener("DOMContentLoaded", main);
