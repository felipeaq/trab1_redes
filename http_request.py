import socket

class HttpRequest(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def make_request(self,link,server,port=80,message_lenght=256,max_len=2**20):
        data="erro na conexão com servidor: {}".format(server)
        if not "http://" in link:
            link="http://"+link
        message="GET "+link+"\r\n"
        print (message)
        server_address = (server, port)
        try:
            self.connect(server_address)
        except:
            return "servidor não econtrado"
        try:
            self.sendall(message.encode())
            temp="bla"
            data=b""
            l=0
            while temp and l<max_len:
                temp=self.recv(message_lenght)
                data+=temp
                l+=message_lenght
        finally:
            self.close()
        return data

if __name__=="__main__":
    '''
    GET http://economia.awesomeapi.com.br/all/USD-BRL
    economia.awesomeapi.com.br 80
    '''
    h=HttpRequest()
    print (h.make_request("http://query1.finance.yahoo.com/v7/finance/options/AAPL","query1.finance.yahoo.com"))

