import socket 
import sys 


def main(port):
    #Create socket connection, and connect 
    client = socket.socket()
    server = socket.gethostbyname(socket.gethostname())
    client.connect(('127.0.0.1', port))

    #Create and send HTTP request 
    request = f'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n'
    request = request.encode('utf-8')
    client.sendall(request)

    #Receive web response 
    data_recv = b''
    while True:
        d = client.recv(4096)
        if not d:
            break
        data_recv += d

    data_recv = data_recv.decode('utf-8')
    print(f'Received:\r\n{data_recv}')
    client.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 your_script.py <port>')
        sys.exit(1)
    port = int(sys.argv[1])
    main(port)
        

