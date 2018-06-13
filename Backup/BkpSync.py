# -*- coding: utf8 -*-
import threading
import client
import server
import notify
import util
import sys
import time
flag_send = 0

if __name__== "__main__":
    if len(sys.argv) < 2:
        print "Modo de uso: python BkpSync.py <arquivo texto de configuração>"
        exit(1)
    f = open(sys.argv[1])
    (ip_client, dire_client, port_client, ip_server, dire_server, port_server) = util.read_file(f)
    ip_client, dire_client, port_client = util.format_config(ip_client, dire_client, port_client)
    ip_server, dire_server, port_server = util.format_config(ip_server, dire_server, port_server)
    th = threading.Thread(target=client.client, args=(dire_client, ip_client, port_client))
    th.daemon = True
    th.start()
    s = server.server(dire_server, ip_server, port_server)