# Realtime-Python-OCR

<!-- TABLE OF CONTENTS -->
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#teck-stack">Teck Stack</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>


<!-- ABOUT THE PROJECT -->
## About The Project

This project is a real-time Optical Character Recognition (OCR) system built with Python that combines both backend processing and frontend visualization into a unified full-stack application.

On the backend, which is powered by FastAPI, the system captures and preprocesses live frames from a phone camera stream using OpenCV and NumPy. Text regions are first detected using a CRAFT-based text detector. These detected regions are then passed to TrOCR (Transformer-based OCR) for text recognition.

On the frontend, a JavaScript-based web interface displays the live camera frame alongside the latest recognized text results, showing real-time results to the users.

For remote access and testing across devices and networks, I also used Tailscale, enabling secure peer-to-peer connectivity without complex port forwarding or public deployment. This allowed seamless access to the FastAPI server from different devices during development and demonstration.

### Tech Stack

