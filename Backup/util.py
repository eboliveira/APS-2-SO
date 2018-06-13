# -*- coding: utf-8 -*-
import os
import sys

def format_message(message):    #formata a mensagem numa string, para enviar pelo socket
    mes = str(message['header'].mask)
    mes = mes + "*"             #token para separar os campos
    mes+= str(message['type_name'])
    mes += "*"
    mes += str(message['filename'])
    mes += '*'
    mes += str(message['patch'])
    return mes

def decode_message(message):    #decodifica a mensagem, ou seja, tira da string e passa para uma lista
    message = message.split('*')
    return message

def position(path): #recebe o caminho da outra máquina e posiciona para a mesma pasta da outra máquina, porém, na sua máquina
    dire = path.split('/')  #passa para uma lista para poder percorrer
    i = 0
    while dire[i] != "BkpSync": #posiciona até encontrar a pasta BkpSync
        i += 1
    i+=1
    directory = "/"     #adiciona a barra que foi tirada na primeira linha
    while i < len(dire):
        directory += dire[i]    #preenche o caminho relativo após a pasta BkpSync
        directory += '/'
        i+=1
    dire = os.getcwd()          #pega o diretório atual
    dire += directory           #coloca o restante
    return dire

def delete_folder(path, foldername):    #deleta uma pasta
    dire = position(path)
    dire += foldername
    if os.path.exists(dire):            #se a pasta existir
        command = "rm -r " + dire
        os.system(command)

def create_folder(path, foldername):    #cria uma pasta
    dire = position(path)
    dire += foldername
    if not os.path.exists(dire):        #se a pasta não existir
        command = "mkdir " + dire
        os.system(command)

def create_file(path, filename):        #cria um arquivo
    dire = position(path)
    if not os.path.exists(dire):
        command = "mkdir " + dire
        os.system(command)
    dire += filename
    if not os.path.isfile(dire):        #se o arquivo não existir
        f = open(dire,'wb')
        f.close()

def delete_file(path, filename):        #deleta um arquivo
    dire = position(path)
    dire += filename
    if os.path.isfile(dire):            #se ele existir
        command = "rm " + dire
        os.system(command)

def modify_file(path, filename, conn):  #protocolo para receber um arquivo
    tam = int(conn.recv(1024))          #recebe o tamanho
    delete_file(path, filename)         #deleta o anterior (lógica de overwrite)
    dire = position(path)               #
    dire += filename                    #pega o arquivo com o diretório absoluta
    f_act = open(dire,'wb')             #abre o arquivo para escrita binária
    f = conn.recv(1024)                 #recebe a primeira parte do arquivo
    f_act.write(f)                      #escreve no arquivo criado
    f_act.close()                       #fecha o arquivo
    tam -= 1024                         #decrementa o tamanho
    while tam > 0 :                     #verifica se tem mais arquivo para receber
        f_act = open(dire,'ab')         #abre o arquivo e escreve no final (append), binario
        f = conn.recv(1024)             #recebe a parte do arquivo
        tam_act = len(f)                #tamanho atual é o tamanho da partição do arquivo que foi recebida
        f_act.write(f)                  #escrevendo no nosso arquivo
        tam -= tam_act                  #decrementamos o restante
    conn.sendall("ack")                 #enviamos um ack para o server


def format_config(ip, dire, port):
    i = 0
    ip = ip.replace(' ','')
    dire = dire.replace(' ','')
    port = port.replace(' ','')
    ip = ip.strip('\n')
    dire = dire.strip('\n')
    port = port.strip('\n')
    while ip[i] != '=':
        i+=1
    i+=1
    ip = ip[i:]
    i = 0
    while dire[i] != '=':
        i+=1
    i+=1
    dire = dire[i:]
    i = 0
    while port[i] != '=':
        i+=1
    i+=1
    port = port[i:]
    return ip,dire,port

def read_file(f):
    f.readline()
    ip_cliente = f.readline()
    dire_client = f.readline()
    port_client = f.readline()
    f.readline()
    ip_servidor = f.readline()
    dire_servidor = f.readline()
    port_servidor = f.readline()
    return ip_cliente, dire_client, port_client, ip_servidor, dire_servidor, port_servidor




