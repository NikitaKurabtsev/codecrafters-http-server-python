import socket
import sys
import os
from typing import List
from threading import Thread

HTTP_200 = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
HTTP_404 = bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8")
CONTENT_TYPE_TEXT = bytes("Content-Type: text/plain\r\n", "utf-8")
CONTENT_TYPE_APP = bytes("Content-Type: application/octet-stream\r\n", "utf-8")
CONTENT_LENGTH = bytes("Content-Length: ", "utf-8")


def generate_response(content: bytes, content_type: bytes) -> bytes:
    content_length = str(len(content))
    return (
        HTTP_200
        + content_type
        + CONTENT_LENGTH
        + bytes(content_length, "utf-8")
        + b"\r\n\r\n"
        + content
    )


def process_request(path: bytes, headers: List[bytes]) -> bytes:
    match path:
        case b"/":
            response = HTTP_200 + b"\r\n"
        case _ if path.startswith(b"/echo/"):
            content = path.lstrip(b"/echo/")
            response = generate_response(content, CONTENT_TYPE_TEXT)
        case _ if path.startswith(b"/user-agent"):
            content = headers[2].split(b" ")[-1]
            response = generate_response(content, CONTENT_TYPE_TEXT)
        case _ if path.startswith(b"/files/") and sys.argv[1] == "--directory":
            filename = path.lstrip(b"/files/")
            directory = sys.argv[2]
            filepath = os.path.join(directory, filename.decode())
            match filepath:
                case _ if os.path.exists(filepath):
                    with open(filepath, 'rb') as file:
                        content = file.read()
                        print(content)
                        response = generate_response(content, CONTENT_TYPE_APP)
                case _:
                    response = HTTP_404
        case _:
            response = HTTP_404

    return response


def handle_connection(client_connection: socket.socket) -> None:
    data = client_connection.recv(1024)

    http_headers = data.split(b"\r\n")
    path = data.split(b" ")[1]

    response = process_request(path, http_headers)

    client_connection.sendall(response)


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket = server_socket.accept()[0]

        thread = Thread(target=handle_connection, args=[client_socket])
        thread.start()


if __name__ == "__main__":
    main()
