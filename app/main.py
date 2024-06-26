import socket
import sys
import os
from typing import List
from threading import Thread

from app.constants import (
    SERVER_HOST,
    SERVER_PORT,
    HTTP_200,
    HTTP_201,
    HTTP_400,
    HTTP_404,
    GET,
    POST,
    MAX_BUFFER_SIZE
)


def response_handler(content: bytes, file: bool = False) -> bytes:
    content_length = str(len(content)).encode("utf-8")
    content_type = b"application/octet-stream" if file else b"text/plain"

    return (
        HTTP_200
        + (b"Content-Type: " + content_type + b"\r\n")
        + (b"Content-Length: " + content_length)
        + b"\r\n\r\n"
        + content
    )


def request_handler(request_data: List[bytes], http_method: bytes, path: bytes) -> bytes:
    if path == b"/":
        response = HTTP_200 + b"\r\n"

    elif path.startswith(b"/echo/"):
        content = path.lstrip(b"/echo/")
        response = response_handler(content)

    elif path.startswith(b"/user-agent"):
        content = request_data[2].split(b" ")[-1]
        response = response_handler(content)

    elif path.startswith(b"/files/") and sys.argv[1] == "--directory":
        filename = path.lstrip(b"/files/")
        directory = sys.argv[2]
        filepath = os.path.join(directory, filename.decode())

        if http_method == GET:
            if os.path.exists(filepath):
                with open(filepath, "rb") as file:
                    content = file.read()
                    response = response_handler(content, file=True)
            else:
                response = HTTP_404[:-2] + b"Content-Length: 0\r\n\r\n"

        elif http_method == POST:
            with open(filepath, "wb") as file:
                content = request_data[-1]
                file.write(content)
                response = HTTP_201
        else:
            response = HTTP_400
    else:
        response = HTTP_404

    return response


def connection_handler(client_connection: socket.socket) -> None:
    data = client_connection.recv(MAX_BUFFER_SIZE)

    http_method = data.split(b" ")[0]
    request_data = data.split(b"\r\n")
    path = data.split(b" ")[1]

    response = request_handler(request_data, http_method, path)

    client_connection.sendall(response)


def main():
    server_socket = socket.create_server((SERVER_HOST, SERVER_PORT), reuse_port=True)

    while True:
        client_socket = server_socket.accept()[0]
        thread = Thread(target=connection_handler, args=[client_socket])
        thread.start()


if __name__ == "__main__":
    main()
