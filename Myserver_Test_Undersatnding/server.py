import socket
import sys

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

        data_recv = b''
        while True:
            data = client_socket.recv(4096) # Take parameter how many bytes to be recived  
            if len(data) == 0:
                break
            data_recv += data
            #if code below not added, loop is stuck 
            if b'\r\n\r\n' in data_recv:
                break  # Break if we've received the end of the request header
            
        #Send simple respone 
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello World'
        response = response.encode('utf-8')
        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 your_script.py <port>')
        sys.exit(1)
    port = int(sys.argv[1])
    main(port)


