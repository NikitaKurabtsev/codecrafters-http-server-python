import socket
from typing import List

HTTP_200 = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
HTTP_404 = bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8")
CONTENT_TYPE = bytes("Content-Type: text/plain\r\n", "utf-8")
CONTENT_LENGTH = bytes("Content-Length: ", "utf-8")


def generate_response(content: bytes) -> bytes:
    content_length = str(len(content))
    return (
        HTTP_200
        + CONTENT_TYPE
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
            response = generate_response(content)
        case _ if path.startswith(b"/user-agent"):
            content = headers[2].split(b" ")[-1]
            response = generate_response(content)
        case _:
            response = HTTP_404

    return response


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, host = server_socket.accept()

    data = conn.recv(1024)

    http_headers = data.split(b"\r\n")
    path = data.split(b" ")[1]
    response = process_request(path, http_headers)

    conn.sendall(response)


if __name__ == "__main__":
    main()
