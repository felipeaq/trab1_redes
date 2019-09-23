import socket
import sys

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (sys.argv[1], int(sys.argv[2]))
    print ( 'connecting...') 
    sock.connect(server_address)
    try:
        for message in sys.stdin:

           print ('received {}'.format(message))
           sock.sendall(message.encode())
           amount_received = 0
           amount_expected = len(message)
           data = sock.recv(4096)
           print ('received {}'.format(data.decode()))

    finally:
        print( 'closing socket')
        sock.close()
if __name__=="__main__":
    if len(sys.argv)==3:
        main()
    else:
        print ("a execução deve seguir o padrão: \n\
            python client.py <ip> <port> \n\
            exemplo python client.py 127.0.0.1 5000 ")