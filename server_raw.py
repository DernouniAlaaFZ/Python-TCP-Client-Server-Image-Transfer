import socket
import struct
import time
import cv2
import numpy as np

PORT = 8080
HEADER_SIZE = 8  # 2 bytes height + 2 bytes width + 4 bytes payload length


def recv_exact(sock, n):
    """Read exactly n bytes from a TCP stream."""
    data = bytearray()

    while len(data) < n:
        chunk = sock.recv(n - len(data))

        if not chunk:
            return None

        data.extend(chunk)

    return bytes(data)


def calculate_psnr(img1, img2):
    """Evaluate the quality of reconstructed images using PSNR."""
    mse = np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(1)

    print(f"Server listening on port {PORT}...")
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    try:
        # Wait for the first byte without consuming it.
        if not conn.recv(1, socket.MSG_PEEK):
            print("Client closed the connection without sending data.")
            return

        start_time = time.time()

        # TODO 5: Read the exact header bytes.
        header = recv_exact(conn, HEADER_SIZE)

        if header is None:
            print("Error: Connection closed before the complete header was received.")
            return

        # TODO 6: Unpack the header fields.
        height, width, payload_length = struct.unpack('!HHI', header)

        print(f"Header received: {width}x{height}, payload = {payload_length} bytes")

        # TODO 7: Read the exact image payload.
        payload = recv_exact(conn, payload_length)

        if payload is None:
            print("Error: Connection closed before the complete image payload was received.")
            return

        # TODO 8: Reconstruct the image by decoding the compressed payload.
        nparr = np.frombuffer(payload, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print("Error: Failed to decode the received compressed image payload.")
            return

        # Save the received image.
        output_path = "received_image.png"
        save_success = cv2.imwrite(output_path, img)

        if save_success:
            print(f"Received compressed image saved successfully: {output_path}")
        else:
            print("Error: Could not save the received image.")

        # Evaluate the quality of reconstructed images
        original_img_path = "test_image.png"
        original_img = cv2.imread(original_img_path)

        if original_img is not None and original_img.shape == img.shape:
            psnr_value = calculate_psnr(original_img, img)
            print(f"Quality Evaluation | PSNR: {psnr_value:.2f} dB")
        else:
            print("Quality Evaluation | Original reference image not found for comparison.")

        # TODO 9: Calculate network performance metrics.
        elapsed = time.time() - start_time
        latency_ms = elapsed * 1000
        packet_loss = 0.0
        throughput_kbps = (
            payload_length / (elapsed * 1024) if elapsed > 0 else 0.0
        )

        print(f"Compressed Transfer Complete | Size: {HEADER_SIZE + payload_length} bytes")
        print(
            f"Metrics | Latency: {latency_ms:.3f} ms | "
            f"Packet loss: {packet_loss:.2f} % | "
            f"Throughput: {throughput_kbps:.2f} KB/s"
        )

    finally:
        conn.close()
        server_socket.close()


if __name__ == '__main__':
    run_server()
