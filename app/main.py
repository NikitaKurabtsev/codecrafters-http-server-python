import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, host = server_socket.accept()

    data = conn.recv(1024)

    http_method, path, http_version, *rest = data.split(b" ")
    print(path)

    if path == b"/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith(b"/echo/"):
        body = path.lstrip("/echo/")
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n\r\n"
            f"{body}"
        )
    else:
        print(f"Something goes wrong: {e}")
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"

    conn.sendall(response.encode())
    print(f"Connection from: {host}, received: {data}")

if __name__ == "__main__":
    main()
