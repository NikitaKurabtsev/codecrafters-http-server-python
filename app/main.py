import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, host = server_socket.accept()

    HTTP_200 = bytes("HTTP/1.1 200 OK\r\n\r\n")
    HTTP_400 = bytes("HTTP/1.1 400 Bad Request\r\n\r\n")
    HTTP_404 = bytes("HTTP/1.1 404 Not Found\r\n\r\n")

    data = conn.recv(1024)

    try:
        http_method, path, http_version, *rest = data.split(b" ")
        print(path)

        if path == b"/":
            conn.sendall(HTTP_200)
        else:
            conn.sendall(HTTP_404)

    except Exception as e:
        print(f"Something goes wrong: {e}")
        conn.sendall(HTTP_400)

    print(f"Connection from: {host}, received: {data}")

if __name__ == "__main__":
    main()
