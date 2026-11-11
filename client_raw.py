import socket
import struct
import time
import cv2
import numpy as np
 
SERVER_IP = '127.0.0.1'
PORT = 8080
 
 
def generate_test_image(IMAGE_PATH, width, height):
    image = np.full((height, width, 3), 40, dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            image[y, x, 0] = int((x / width) * 255)
            image[y, x, 1] = int((y / height) * 255)
    center_coordinates = (width // 2, height // 2)
    cv2.circle(image, center_coordinates, 80, (0, 0, 255), -1)
    cv2.rectangle(image, (50, 50), (200, 150), (0, 255, 255), 3)
    cv2.line(image, (50, height - 50), (width - 50, height - 50), (0, 255, 0), 4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, 'TCP IMAGE TEST', (width // 2 - 140, 60),
                font, 1.0, (255, 255, 255), 2)
    cv2.putText(image, f'{width}x{height} px', (width // 2 - 60, height // 2 + 120),
                font, 0.7, (255, 255, 255), 1)
    cv2.imwrite(IMAGE_PATH, image)
 
 
def run_client():
    IMAGE_PATH = "test_image.png"
    width = 640
    height = 480
    mode = "compressed-jpeg"
 
    # TODO 1: Generate the test image
    generate_test_image(IMAGE_PATH, width, height)
 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Disable Nagle's algorithm so that small sends are not delayed for merging.
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client_socket.connect((SERVER_IP, PORT))
    print(f"Connected to server at {SERVER_IP}:{PORT} (mode: {mode})")
 
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        print(f"Error: {IMAGE_PATH} not found.")
        client_socket.close()
        return
 
    # TODO 2: Extract height, width and channels from the image shape, with JPEG compression
    h, w, channels = img.shape
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
    success, encoded_image = cv2.imencode('.jpg', img, encode_param)
    if not success:
        print("Error: Image compression failed.")
        client_socket.close()
        return

    payload = encoded_image.tobytes()
    payload_length = len(payload)
 
    try:
        start_time = time.time()
 
        # TODO 3: Construct the fixed-size header:
        # Height (2 bytes), Width (2 bytes), Payload length (4 bytes)
        header = struct.pack('!HHI', h, w, payload_length)
 
        # TODO 4: Send the header and the compressed image payload
        client_socket.sendall(header)
        client_socket.sendall(payload)
        calls = 2  # Header send + Payload send
 
        elapsed = time.time() - start_time
        throughput = payload_length / (elapsed * 1000000) if elapsed > 0 else 0
        print(f"Sent compressed image {w}x{h} "
              f"({payload_length} bytes) in {elapsed:.4f} seconds "
              f"using {calls} send call(s) ({throughput:.2f} MB/s).")
    finally:
        client_socket.close()
 
 
if __name__ == '__main__':
    run_client()
