import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, host = server_socket.accept()

    HTTP_200 = bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8")
    HTTP_200_ONE_LINE = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
    HTTP_400 = bytes("HTTP/1.1 400 Bad Request\r\n\r\n", "utf-8")
    HTTP_404 = bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8")
    CONTENT_TYPE = bytes("Content-Type: text/plain\r\n", "utf-8")

    data = conn.recv(1024)

    try:
        http_method, path, http_version, *rest = data.split(b" ")
        print(path)

        if path == b"/":
            response = HTTP_200
        elif path.startswith(b"/echo/"):
            content = path.lstrip(b"/echo/")
            content_length = len(content)
            response = (
                    HTTP_200_ONE_LINE
                    + CONTENT_TYPE
                    + b"Content-Length: "
                    + bytes(content_length)
                    + b"\r\n\r\n"
                    + content
            )
        else:
            response = HTTP_404

    except Exception as e:
        print(f"Something goes wrong: {e}")
        response = HTTP_400

    conn.sendall(response)
    print(f"Connection from: {host}, received: {data}")

if __name__ == "__main__":
    main()
