import socket
import sys

def run_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Set payload, Content-Type, and Content-Length
    payload = 'This is a payload'
    content_type = 'text/plain'
    content_length = len(payload)

    # Construct HTTP request with payload, Content-Type, and Content-Length headers
    request = f'POST / HTTP/1.1\r\n'
    request += f'Content-Type: {content_type}\r\n'
    request += f'Content-Length: {content_length}\r\n\r\n'
    request += payload
    
    request = request.encode("utf-8")
    client.sendall(request)

    response = b''
    while True:
        d = client.recv(4096)
        
        if len(d) == 0:
            break
        response += d
    
    response = response.decode("utf-8")

    print(f"Received: {response}")

    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    run_client(host, port)
