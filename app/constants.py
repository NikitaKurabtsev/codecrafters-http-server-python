SERVER_HOST = "localhost"
SERVER_PORT = 4221

HTTP_200 = bytes("HTTP/1.1 200 OK\r\n", "utf-8")
HTTP_201 = bytes("HTTP/1.1 201 Created\r\n\r\n", "utf-8")
HTTP_400 = bytes("HTTP/1.1 400 Bad Request\r\n\r\n", "utf-8")
HTTP_404 = bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8")

GET = bytes("GET", "utf-8")
POST = bytes("POST", "utf-8")

MAX_BUFFER_SIZE = 1024
