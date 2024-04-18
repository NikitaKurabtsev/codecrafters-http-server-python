import socket
import sys
import os
from typing import List
from threading import Thread

HTTP_200 = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
HTTP_201 = bytes("HTTP/1.1 201 Created\r\n\r\n", "utf-8")
HTTP_404 = bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8")


def generate_response(content: bytes, file: bool = False) -> bytes:
    content_length = str(len(content)).encode("utf-8")
    content_type = b"application/octet-stream" if file else b"text/plain"

    return (
        HTTP_200
        + (b"Content-Type: " + content_type + b"\r\n")
        + (b"Content-Length: " + content_length)
        + b"\r\n\r\n"
        + content
    )


def process_request(request_data: List[bytes], http_method: bytes, path: bytes) -> bytes:
    if path == b"/":
        response = HTTP_200 + b"\r\n"

    elif path.startswith(b"/echo/"):
        content = path.lstrip(b"/echo/")
        response = generate_response(content)

    elif path.startswith(b"/user-agent"):
        content = request_data[2].split(b" ")[-1]
        response = generate_response(content)

    elif path.startswith(b"/files/") and sys.argv[1] == "--directory":
        filename = path.lstrip(b"/files/")
        directory = sys.argv[2]
        filepath = os.path.join(directory, filename.decode())

        if http_method == b"GET":
            if os.path.exists(filepath):
                with open(filepath, "rb") as file:
                    content = file.read()
                    response = generate_response(content, file=True)
            else:
                response = HTTP_404[:-2] + b"Content-Length: 0\r\n\r\n"

        elif http_method == b"POST":
            with open(filepath, "wb") as file:
                content = request_data[-1]
                file.write(content)
                response = HTTP_201
        else:
            response = HTTP_404
    else:
        response = HTTP_404

    return response


def handle_connection(client_connection: socket.socket) -> None:
    data = client_connection.recv(1024)

    http_method = data.split(b" ")[0]
    request_data = data.split(b"\r\n")
    path = data.split(b" ")[1]

    response = process_request(request_data, http_method, path)

    client_connection.sendall(response)


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket = server_socket.accept()[0]

        thread = Thread(target=handle_connection, args=[client_socket])
        thread.start()


if __name__ == "__main__":
    main()
