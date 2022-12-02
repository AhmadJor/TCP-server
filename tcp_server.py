import socket, sys, os
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12345))
server.listen(5)
while True:
    client_socket, client_address = server.accept()
    data = client_socket.recv(100)
    lines = data.decode().split('\r\n')
    file_name = "files" + lines[0].split(" ")[1]
    if os.path.exists(file_name):
        print(data.decode())
        for line in lines:
            if line.split(" ")[0] == 'Connection:':
                connection = line.split(" ")[1]
        size = os.path.getsize(file_name)
        client_socket.send(("HTTP/1.1 200 OK\r\nConnection: " + connection +"\r\nContent-Length: {size}\r\n\r\n").encode())
        file = open(file_name, "rb")
        content = file.read()
        client_socket.send(content)
        file.close()
        if connection == 'closed':
            client_socket.close()
    else:
        client_socket.send("HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode())
        client_socket.close()


