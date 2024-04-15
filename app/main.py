import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, host = server_socket.accept()

    data = conn.recv(4)
    conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    print(f"Connection from: {host}, recieved: {data}")

if __name__ == "__main__":
    main()
