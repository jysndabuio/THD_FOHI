import socket
import sys
import os
import mimetypes

def main(port):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Port to be define by user; IP to be set to what is available.
    server.bind(('127.0.0.1', port))
    #Listen to any connection request 
    server.listen(5)
    print(f'Server listening on port {port}...')

    
    while True:
        client_socket, client_address = server.accept()
        print(f'Connection from {client_address}')

        handle_connection(client_socket)

def handle_connection(client_socket):
    data_recv = b''
    while True:
        data = client_socket.recv(4096) # Take parameter how many bytes to be recived  
        if len(data) == 0:
            break
        data_recv += data
        #if code below not added, loop is stuck 
        if b'\r\n\r\n' in data_recv:
            break  # Break if we've received the end of the request header
    #Decode the data received    
    data_recv = data_recv.decode('utf-8')
    #Parsing the Request Header
    http_header = data_recv.split('\r\n')
    #Stripping the Path down to the Filename
    http_request = http_header[0].split(' ')

    home_dir = os.path.abspath('.')
    #os.path.join(home_dir, http_request[1]) does not work
    full_path = home_dir + os.path.sep + http_request[1]
    full_path = os.path.abspath(full_path)
        
    check_path(client_socket, full_path, home_dir, http_request)

    client_socket.close()

def check_path(client_socket, full_path, home_dir, http_request):
    if not full_path.startswith(home_dir):
        response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length:15 \r\nConnection: close\r\n\r\n404 not found'
        response = response.encode('utf-8')
        client_socket.sendall(response)
    elif full_path.startswith(home_dir):
        try:
            with open(full_path, 'rb') as fp:
                data = fp.read()
                content_type = get_content_type(http_request)
                content_len = len(data)
                response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {content_len}\r\n\r\n'
                response = response.encode('utf-8') + data
                client_socket.sendall(response)
        except Exception as e:
            print(f"Error opening file: {e}")
            response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length:13 \r\nConnection: close\r\n\r\n404 not found'
            response = response.encode('utf-8')
            client_socket.sendall(response)

        

def get_content_type(http_request):
    full_path = os.path.split(http_request[1])
    file_name  = os.path.splitext(full_path[1])
    if file_name[1] in mimetypes.types_map:
        return mimetypes.types_map[file_name[1]]
    else: 
        return None 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 your_script.py <port>')
        sys.exit(1)
    port = int(sys.argv[1])
    main(port)


