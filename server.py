# -*- coding: utf-8 -*-
import socket
import notify
import threading
import sys
import util
import os
import time

class server(object):

    '''
    No construtor da classe, definimos que diretório padrão é o atual, o host padrão é o que retorna da
    função socket.gethostname() e a porta padrão é a 50007 que é uma porta não usada
    '''
    def __init__(self,dire = os.getcwd(), host = socket.gethostname(), port = 50007):
        self.eventos = []       #inicia um vetor que vai armazer todos os eventos
        th = threading.Thread(target=notify.monitorar, args=(self.eventos,dire))    #inicia uma thread para monitorar e passa
                                                                                    # o vetor para ir colocando os eventos
        th.daemon = True      #variavel para a thread morrer junto com o processo
        th.start()            #inicia a thread
        time.sleep(1)         #espera a pasta ser criada na thread de monitorar
        dire = os.getcwd()    #pega o diretório atual
        dire += "/BkpSync"    #
        os.chdir(dire)        #Muda o diretório do nosso programa para a pasta do BkpSync
        self.server = socket.socket()   #inicia um socket
        self.server.connect((host, port))   #tenta conectar ao socket referenciado por parametro
        self.send()                         #chama a função de mandar mensagem
        
    
    def send(self):
        while True:         #faz para sempre, até que o programa morra
            while len(self.eventos):    #verifica se tem eventos
                th = threading.Thread(target = self.event())    #cria uma thread para enviar o evento
                th.daemon = True     #variavel para a thread morrer junto com o processo
                th.start()           #inicia a thread

    
    def event(self):
        mes = self.eventos.pop()    #passa para a variavel mes o evento que foi gerado
        mes1 = mes                  #faz uma cópia desse evento
        mes = util.format_message(mes)      #formata a mensagem em string para mandar pelo socket
        self.server.sendall(mes)            #envia a mensagem toda de controle
        print mes                           #printa a mensagem enviada
        print self.server.recv(1024)        #printa a resposta do cliente
        if int(mes1['header'].mask) == notify.MODIFY_FILE or int(mes1['header'].mask) == notify.FILE_MOVE_TO:   #verifico se é uma modificação ou um move_to
            message = util.decode_message(mes)      #decodifico a mensagem enviada
            self.send_file(message)                 #chama a função de enviar arquivo


    def send_file(self, mes):
        dire = mes[3] + '/' + mes[2]        #concatena diretório com o arquivo
        time.sleep(0.1)                     #evita o bug de ler o tamanho do arquivo como 0
        tam = os.path.getsize(dire)         #vejo o tamanho do arquivo
        self.server.sendall(str(tam))       #envio pro cliente o tamanho do arquivo que vou enviar
        f = open(dire, 'rb')                #abro o arquivo para leitura
        while tam > 0:                      #enquanto tiver arquivo para enviar
            if tam > 1024:                  #
                content = f.read(1024)      #
                tam-=1024                   #
            else:                           #envio o arquivo particionado
                content = f.read(tam)       #
                tam -= tam                  #
            self.server.send(content)       #
        f.close()                           #fecho o arquivo
        print self.server.recv(1024)        #printo a resposta do cliente (deve ser um ok)
                
if __name__ == "__main__":

    #<Diretorio> <hostname> <porta>
    if len(sys.argv) == 1:      #se passar somente um argumento, ou seja, só o python server.py, chama o construtor sem nada
        s = server()      
    elif len(sys.argv) == 2:    #se passar somente um argumento além do arquivo, deve ser o diretório
        s = server(sys.argv[1])
    elif len(sys.argv) == 3:    #se passar dois argumentos além do arquivo, deve ser o diretório e o hostname
        s = server(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:    #se passar três argumentos além do arquivo, deve ser o diretório, o hostname e a porta
        s = server(sys.argv[1], sys.argv[2], sys.argv[3])
