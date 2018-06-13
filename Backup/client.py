# -*- coding: utf-8 -*-
import socket
import notify
import util
import os
import sys
import threading
import time
import BkpSync

class client (object):

    def __init__(self, dire, host, port):
        if not dire:
            dire = os.getcwd()
        if not host:
            host = socket.gethostname()
        if not port:
            port = 50007
        dire += '/BkpSync'
        if not os.path.exists(dire):        #Altera o diretório para a pasta BkpSync, se não tiver, cria esta pasta
            os.mkdir(dire)                  #
        os.chdir(dire)                      #
        self.s = socket.socket()            #Cria o socket
        self.s.bind((host,int(port)))       #Define que ele vai quem vai escutar
        self.s.listen(1)                    #escuta
        self.conn, self.addr = self.s.accept()  #aceita e estabelece conexão
        self.receive()                      #chama a função de receber

    def receive(self):
         while True:        #vai ficar recebendo até o processo morrer
            mes = self.conn.recv(1024)  #recebe a mensagem do servidor
            mes = util.decode_message(mes)  #decodifica a mensagem do servidor
            print mes
            self.conn.sendall("receive")    #avisa o servidor que recebeu a mensagem
            self.decode(mes)                #chama a função que define qual o destino à ser tomado


    def decode(self, message):
        mask = int(message[0])      #mascara
        filename = message[2]       #nome do arquivo
        path = message[3]           #caminho
        if mask == notify.CREATE_DIR:   #se for uma mensagem de criar pasta, chama a função que cria pasta, e assim por diante, para todas as máscaras
            util.create_folder(path, filename)
        elif mask == notify.DELETE_DIR:
            util.delete_folder(path,filename)
        elif mask == notify.CREATE_FILE:
            util.create_file(path, filename)
        elif mask == notify.DELETE_FILE:
            util.delete_file(path,filename)
        elif mask == notify.MODIFY_FILE:
            BkpSync.flag_send = 1
            time.sleep(1)
            util.modify_file(path, filename, self.conn)
            time.sleep(1)
            BkpSync.flag_send = 0
        elif mask == notify.DIR_MOVED_FROM:
            util.delete_folder(path,filename)
        elif mask == notify.DIR_MOVED_TO:
            util.create_folder(path,filename)
        elif mask == notify.FILE_MOVED_FROM:
            util.delete_file(path,filename)
        elif mask == notify.FILE_MOVE_TO:
            BkpSync.flag_send = 1
            time.sleep(1)
            util.modify_file(path, filename, self.conn)
            time.sleep(1)
            BkpSync.flag_send = 0
        
