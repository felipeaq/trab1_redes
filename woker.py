import random
import json
import socket
from http_request import HttpRequest

class ExternalFiles: # classe que contém links externos
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
        #dicionario de metodos:
        self.methods={"\\verlivros":self.books,"\\verdolar":self.dollar2real,"\\veracao":self.stock_price} 
        self.timeout=timeout
        self.external_files=ExternalFiles("bibliografias.txt",
            "economia.awesomeapi.com.br",
            "economia.awesomeapi.com.br/all/USD-BRL",
            "/api/v3/stock/real-time-price/",
            "financialmodelingprep.com")

    def get_message(self,data):
        #processa a mensagem do cliente
        message_list=[]
        try:
            message_list=data.decode().split()
        except:
            print ("mensagem impossível de decodificar") # se for algo tipo um crtl+c, retorna mensagem de erro
        if not message_list: #se não ouver nada na mensagem, retorna vazio
            return ""
        message=message_list[0]
        args=[]
        if len(message_list)>1: # fazer parser dos argumentos do comando
            args=message_list[1:]
        print (message.encode())
        if not message in self.methods.keys(): # se não for uma palavra reservada, então retorna a propria palavra
            return message
        return self.methods[message](*args) #retorna a palvra correspondente ao método

    def execute(self):
        data = "bla"
        self.conn.settimeout(self.timeout)
        while data: #recebe mensagem responde
            try:
                data= self.conn.recv(32)
                message=self.get_message(data)
                self.conn.sendall(message.encode())
            except socket.timeout: #aguarda algum tempo, caso de timeout ele desconecta
                print ("timeout no cliente",self.client)
                data=None
        self.conn.close()
            
    def books(self,*args): #metodo que retona um livro aleatório sobre investimento
        f=open(self.external_files.book_file,"r")
        book_list=f.read().split("<>")
        return random.choice(book_list)

    def dollar2real(self,*args): #metodo que converte 1 dolar em real em um servidor externo e retona
        try:
            h=HttpRequest()
            dollar_string=h.make_request(self.external_files.dollar_link,self.external_files.dollar_server)
            d= json.loads(dollar_string.decode())["USD"]
            message="preço de baixo: {}\npreço de alta: {}\npreço de bid: {}\npreço de ask: {}\n".format(
                d["low"],d["high"],d["bid"],d["ask"])
        except:
            message="impossivel alcançar servidor {}".format(self.external_files.dollar_server)
        return message
    
    def stock_price(self,*args): #metodo que busca preço de ação por palavra chave
        if len(args)!=1:
            return "para ver o preço de ações deve ser passado o nome de uma \
                exemplo: \\veracao AAPL"
        h=HttpRequest()
        try:
            temp= h.make_request(self.external_files.stock_link+args[0],self.external_files.stock_server,port=443)
        except:
            #caso de erro no servidor
            print (self.external_files.stock_server.encode())
            return "impossível conectar ao servidor de terceiro\n"
        try:
            d=json.loads(temp)["price"]
        except KeyError: #caso seja uma ação errada
            return "Ação {} não encontrada\n".format(args[0])
        except json.JSONDecodeError:
            return "Recebemos uma mensagem estranha do servidor externo, nossos engenheiros estão trabalhando nisso".format(args[0])
        except Exception as e:
            print (temp)
            return "Problema com o servidor externo\n"
        return "preço da ação "+args[0]+": "+ str(d)+"\n" #preço formatado da ação
