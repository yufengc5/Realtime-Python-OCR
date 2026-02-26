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

The frameworks/libraries used in this project include:

#### Backend
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
#### Frontend
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
#### Machine Learning Models
[![CRAFT OCR](https://img.shields.io/badge/CRAFT-Text_Detector-blue?style=for-the-badge)]()
[![TrOCR](https://img.shields.io/badge/TrOCR-Transformer_OCR-orange?style=for-the-badge)]()
#### Networking
[![Tailscale](https://img.shields.io/badge/Tailscale-242424?style=for-the-badge&logo=tailscale&logoColor=white)](https://tailscale.com/)

