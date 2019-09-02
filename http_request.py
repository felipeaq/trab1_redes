import socket
import ssl
class HttpRequest(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def make_request(self,link,server,port=80,message_lenght=256,max_len=2**20):
        data="erro na conexão com servidor: {}".format(server) #mensagem default, caso não haja resposta
        server_address = (server, port) 
        try: #tenta conectar ao servidor
            self.connect(server_address)
        except:
            return "servidor não econtrado"
        if port==80: #se a porta for 80 ajusta ao protocolo HTTP
            s=self
            if not "http://" in link:
                link="http://"+link
            message="GET "+link+"\r\n\r\n"
        if port ==443: #se a porta for 443 faz handshake e ajusta ao protocolo HTTPS
            s=ssl.wrap_socket(self, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
            message="GET "+link+"\r\nHost:"+server+"\r\nConnection: close\r\n\r\n"

        try: #manda requisição
            s.sendall(message.encode())
            temp="bla"#qualquer coisa que entre no laço while
            data=b""
            l=0
            while temp and l<max_len: #equanto ouver mais dados e não chegar ao limite, fica lendo a mensagem
                temp=s.recv(message_lenght)
                data+=temp
                l+=message_lenght
        finally:
            s.close()
        return data

if __name__=="__main__":
    '''
    GET http://economia.awesomeapi.com.br/all/USD-BRL
    economia.awesomeapi.com.br 80
    '''
    h=HttpRequest()
    print (h.make_request("/api/v3/stock/real-time-price/AAPL","financialmodelingprep.com",port=443).decode())

