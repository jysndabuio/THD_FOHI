
import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 6060))
s.listen()

#Accept new connection
print('Listening to new connection...')
new_conn, addr = s.accept()
new_socket = new_conn
print(f'Connected to client: {addr[0]}:{addr[1]}')

received_data =  b''
while True:
    data = new_socket.recv(4096)
    if not data:
        break

    received_data += data

# Check if the entire headers have been received
    if b'\r\n\r\n' in received_data:
        # Extract request method
        request_method = received_data.split(b' ')[0].decode('utf-8')
        print(f'Request method: {request_method}')

        # Extract payload
        double_newline_index = received_data.find(b'\r\n\r\n')
        payload = received_data[double_newline_index + 4:].decode('utf-8')
        print(f'Payload from client: {payload}')

        break

response = 'HTTP/1.1 200 OK\r\n\r\nHello, World!'
new_socket.sendall(response.encode('utf-8'))
new_socket.close()

s.close()

