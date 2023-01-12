# coding=utf-8

from ftplib import FTP                                                                      # Importamos la libreria ftplib desde FTP

import sys

def imprimirMensaje():                                                                      # Definimos la funcion para Imprimir el mensaje de bienvenida
    print "------------------------------------------------------"
    print "--               COMMAND LINE EXAMPLE               --"
    print "------------------------------------------------------"
    print ""
    print ">>>             Cliente FTP  en Python                "
    print ""
    print ">>> python <appname>.py <host> <port> <user> <pass>   "
    print "------------------------------------------------------"

def f(s):                                                                                   # Funcion para imprimir por pantalla los datos 
    print s

def download(j):                                                                            # Funcion para descargarnos el fichero que indiquemos según numero    
    print "Descargando=>",files[j]      
    fhandle = open(files[j], 'wb')
    ftp.retrbinary('RETR ' + files[j], fhandle.write)                                       # Imprimimos por pantalla lo que estamos descargando        #fhandle.close()
    fhandle.close()                                                     

ip          = sys.argv[1]                                                                   # Recogemos la IP       desde la linea de comandos sys.argv[1] 
puerto      = sys.argv[2]                                                                   # Recogemos el PUERTO   desde la linea de comandos sys.argv[2]
usuario     = sys.argv[3]                                                                   # Recogemos el USUARIO  desde la linea de comandos sys.argv[3]
password    = sys.argv[4]                                                                   # Recogemos el PASSWORD desde la linea de comandos sys.argv[4]


ftp = FTP(ip)                                                                               # Creamos un objeto realizando una instancia de FTP pasandole la IP
ftp.login(usuario,password)  
