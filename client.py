# -*- coding: utf-8 -*-
import socket
import notify
import util
import os
import sys
import threading

class client (object):

    def __init__(self, dire = os.getcwd(), host = socket.gethostname(), port = 50007):
        dire += '/BkpSync'                  #
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
            util.modify_file(path, filename, self.conn)
        elif mask == notify.DIR_MOVED_FROM:
            util.delete_folder(path,filename)
        elif mask == notify.DIR_MOVED_TO:
            util.create_folder(path,filename)
        elif mask == notify.FILE_MOVED_FROM:
            util.delete_file(path,filename)
        elif mask == notify.FILE_MOVE_TO:
            util.modify_file(path, filename, self.conn)
        


if __name__ == "__main__":
    #<Diretorio> <hostname> <porta>
    if len(sys.argv) == 1:  #se passar somente um argumento, ou seja, só o python server.py, chama o construtor sem nada
        c = client()      
    elif len(sys.argv) == 2:     #se passar somente um argumento além do arquivo, deve ser o diretório
        c = client(sys.argv[1])
    elif len(sys.argv) == 3:    #se passar dois argumentos além do arquivo, deve ser o diretório e o hostname
        c = client(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:    #se passar três argumentos além do arquivo, deve ser o diretório, o hostname e a porta
        c = client(sys.argv[1], sys.argv[2], sys.argv[3])
