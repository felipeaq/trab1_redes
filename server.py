import socket
import sys
import threading
from woker import Worker


class Server:
    def __init__(self,ip,port,n_threads,timeout):
        self.ip=ip
        self.n_threads=n_threads
        self.port = int(port)       
        self.thread_list=[]
        self.timeout=timeout
    
    def start_listening(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip,self.port))
        sock.listen(1)
        while True: #fica escutando sempre, para estabelecer conexão com o cliente
            print ("aguardando conexao...")
            connection, client_address = sock.accept()
            t = threading.Thread(target=self.thread_worker,args=(sock,connection,client_address)) #manda para executar em uma thread
            self.thread_list.append(t) #TODO tirar ou limitar threads
            t.start()

    def thread_worker(self,*args):
        #metodo que funciona paralelo
        w=Worker(args[0],args[1],args[2],timeout=self.timeout)
        w.execute()


def main():
    if (len(sys.argv)!=3):
        print ("execução: python server.py <ip> <porta>")
        print ("exemplo: python server.py 0.0.0.0 5000")
    s= Server(sys.argv[1],sys.argv[2],5,timeout=200)
    s.start_listening()
if __name__=="__main__":
    main()


