# TCP Image Transfer – Client-Server Application

## Project Overview

This project implements a client-server application in Python that enables image transmission over a TCP connection.

The client captures or loads image data and sends it to the server through a TCP socket. The server receives the transmitted data, reconstructs the image, and processes it using OpenCV.

The project demonstrates the fundamentals of network communication, TCP sockets, data serialization, and image processing.

## Technologies Used

- **Python** – Main programming language.
- **Socket** – TCP client-server communication.
- **OpenCV (cv2)** – Image processing and handling.
- **Struct** – Packing and unpacking binary data.

## Project Structure

```text
TCP-Image-Transfer/
│
├── client_raw.py
├── server-raw.py
├── .gitignore
└── README.md
```

## How It Works

1. The server creates a TCP socket and waits for an incoming client connection.
2. The client establishes a connection with the server.
3. The client sends image information and image data over the TCP connection.
4. The server receives the data and reconstructs the image.
5. OpenCV is used to process or display the received image.

## Requirements

- Python 3
- OpenCV

## Installation

Install OpenCV using pip:

```bash
pip install opencv-python
```

## How to Run

**1. Start the server:**

```bash
python server.py
```

**2. Run the client in another terminal:**

```bash
python client.py
```

Make sure the server is running before starting the client.

## Learning Objectives

- Understanding TCP socket communication.
- Implementing client-server architecture.
- Transmitting binary data over a network.
- Handling image data using OpenCV.
- Understanding data serialization using the struct module.

## Project Status

Developed as a practical project for learning and experimenting with Python network programming and image transmission.
