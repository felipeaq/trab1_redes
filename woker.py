import random
import json
from http_request import HttpRequest

class ExternalFiles:
    def __init__(self,book_file,dollar_server,dollar_link,stock_link,stock_server):
        self.book_file=book_file
        self.dollar_server=dollar_server
        self.dollar_link=dollar_link
        self.stock_link=stock_link
        self.stock_server=stock_server

class Worker:
    def __init__(self,sock,conn,client,timeout):
        self.sock=sock
        self.conn=conn
        self.client=client
        self.methods={"\\verlivros":self.books,"\\verdolar":self.dollar2real,"\\veracao":self.stock_price} 
        self.timeout=timeout
        self.external_files=ExternalFiles("bibliografias.txt",
            "economia.awesomeapi.com.br",
            "economia.awesomeapi.com.br/all/USD-BRL",
            "/api/v3/stock/real-time-price/",
            "financialmodelingprep.com")

    def get_message(self,data):
        message_list=[]
        try:
            message_list=data.decode().split()
        except:
            print ("mensagem impossível de decodificar")
        if not message_list:
            return ""
        message=message_list[0]
        args=[]
        if len(message_list)>1:
            args=message_list[1:]
        print (message.encode())
        if not message in self.methods.keys():
            return message
        return self.methods[message](*args)

    def execute(self):
        data = "bla"
        self.conn.settimeout(self.timeout)
        while data:
            try:
                data= self.conn.recv(32)
                message=self.get_message(data)
                self.conn.sendall(message.encode())
            except socket.timeout:
                print ("timeout no cliente",self.client)
                data=None
        self.conn.close()
            
    def books(self,*args):
        f=open(self.external_files.book_file,"r")
        book_list=f.read().split("<>")
        return random.choice(book_list)

    def dollar2real(self,*args):
        try:
            h=HttpRequest()
            dollar_string=h.make_request(self.external_files.dollar_link,self.external_files.dollar_server)
            d= json.loads(dollar_string.decode())["USD"]
            message="preço de baixo: {}\npreço de alta: {}\npreço de bid: {}\npreço de ask: {}\n".format(
                d["low"],d["high"],d["bid"],d["ask"])
        except:
            message="impossivel alcançar servidor {}".format(self.external_files.dollar_server)
        return message
    
    def stock_price(self,*args):
        if len(args)!=1:
            return "para ver o preço de ações deve ser passado o nome de uma \
                exemplo: \\veracao AAPL"
        h=HttpRequest()
        try:
            temp= h.make_request(self.external_files.stock_link+args[0],self.external_files.stock_server,port=443)
        except:
            print (self.external_files.stock_server.encode())
            return "impossível conectar ao servidor de terceiro\n"
        try:
            d=json.loads(temp)["price"]
        except KeyError:
            return "Ação {} não encontrada\n".format(args[0])
        except json.JSONDecodeError:
            return "Recebemos uma mensagem estranha do servidor externo, nossos engenheiros estão trabalhando nisso".format(args[0])
        except Exception as e:
            print (temp)
            return "Problema com o servidor externo\n"
        return "preço da ação "+args[0]+": "+ str(d)+"\n"
