# -*- coding: utf-8 -*-
import os
import logging
import time

import inotify.adapters

#Defines das flags que nos interessa
CREATE_DIR = 1073742080
CREATE_FILE = 256
DIR_MOVED_FROM = 1073741888
DIR_MOVED_TO = 1073741952
MODIFY_FILE = 2
FILE_MOVED_FROM = 64 
FILE_MOVE_TO = 128
DELETE_FILE = 512
DELETE_DIR = 1073742336


eventos_mask = (CREATE_DIR, CREATE_FILE, DIR_MOVED_FROM, DIR_MOVED_TO, DELETE_DIR, DELETE_FILE, MODIFY_FILE, FILE_MOVED_FROM, FILE_MOVE_TO)

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)

def monitorar(eventos, dire):
    _configure_logging()
    dire += "/BkpSync"
    if os.path.exists(dire):
        print("BkpSync dire exists.")
    else:
        print("BkpSync dire not exists, creating...")
        os.mkdir(dire)

    print("Monitoring BkpSync dir...")

    i = inotify.adapters.InotifyTree(dire)

    for event in i.event_gen():
        if event is not None:
            (header, type_names, watch_path, filename) = event
            event = {'header' : header, 'type_name' : type_names, 'patch' : watch_path, 'filename' : filename}
            if header.mask in eventos_mask:     #verifico se a mascara do evento nos interessa (as que nos interessa está em eventos_mask)
                eventos.append(event)           #colocamos na lista que foi passada por paramêtro


