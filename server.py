# -*- coding: utf-8 -*-
import socket
import notify
import threading
import sys
import util
import os
import time
import BkpSync

class server(object):

    '''
    No construtor da classe, definimos que diretorio padrao e o atual, o host padrao e o que retorna da
    funcao socket.gethostname() e a porta padrao e a 50007 que e uma porta nao usada
    '''
    def __init__(self,dire, host, port):
        if not dire:
            dire = os.getcwd()
        if not host:
            host = socket.gethostname()
        if not port:
            port = 50007
        self.eventos = []       #inicia um vetor que vai armazer todos os eventos
        self.flag = 0           #flag para verificar se está conectado
        th = threading.Thread(target=notify.monitorar, args=(self.eventos,dire))    #inicia uma thread para monitorar e passa
                                                                                    # o vetor para ir colocando os eventos
        th.daemon = True      #variavel para a thread morrer junto com o processo
        th.start()            #inicia a thread
        time.sleep(1)         #espera a pasta ser criada na thread de monitorar
        dire = os.getcwd()    #pega o diretorio atual
        os.chdir(dire)        #Muda o diretorio do nosso programa para a pasta do BkpSync
        self.server = socket.socket()   #inicia um socket
        while self.flag == 0:           #fica tentando conectar de 2 em 2 segs
            th = threading.Thread(target=self.conectar, args=(host, int(port))) #cria uma thread, pois a falha na conexão mata o processo
            th.daemon = True
            th.start()                          
            time.sleep(2)
        print "connected"
        self.send()                         #chama a funcao de mandar mensagem

    def conectar(self,host,port):   #conecta
        self.server.connect((host,port))    #a thread sempre morre aqui, caso não consiga a conexão
        self.flag = 1                       #se chegou aqui, quer dizer que a thread conectou
        
    
    def send(self):
        while True:         #faz para sempre, ate que o programa morra
            while len(self.eventos):    #verifica se tem eventos
                th = threading.Thread(target = self.event())    #cria uma thread para enviar o evento
                th.daemon = True     #variavel para a thread morrer junto com o processo
                th.start()           #inicia a thread

    
    def event(self):
        mes = self.eventos.pop()    #passa para a variavel mes o evento que foi gerado
        mes1 = mes                  #faz uma copia desse evento
        mes = util.format_message(mes)      #formata a mensagem em string para mandar pelo socket
        self.server.sendall(mes)            #envia a mensagem toda de controle
        print mes                           #printa a mensagem enviada
        print self.server.recv(1024)        #printa a resposta do cliente
        if int(mes1['header'].mask) == notify.MODIFY_FILE or int(mes1['header'].mask) == notify.FILE_MOVE_TO:   #verifico se e uma modificacao ou um move_to
            message = util.decode_message(mes)      #decodifico a mensagem enviada
            self.send_file(message)                 #chama a funcao de enviar arquivo


    def send_file(self, mes):
        BkpSync.flag_send = 1
        time.sleep(1)
        dire = mes[3] + '/' + mes[2]            #concatena diretorio com o arquivo
        if os.path.exists(dire):
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
            print self.server.recv(1024)        #printo a resposta do cliente (deve ser um ack)
        BkpSync.flag_send = 0
