#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, commands

# Funciones
# Comprueba el número de parámetros
def ComprobarNumParam(numero):
    if numero < 2:
        return(0)
    elif numero > 2:
        return(2)
    else:
        return(1)

# Comprueba el tipo de parámetro introducido
def ComprobarTipoParam(parametro):
    parametroIP = ParamIP(parametro)
    if parametro == "-l":
        return(1)
    elif parametro == "-h":
        return(3)
    elif parametroIP == 1:
        return(2)
    else:
        return(0)

# Comprueba que la IP pasada como argumento sea una dirección IP válida
def ParamIP(ip):
    checkip = ip.split(".")
    ipok = False
    if len(checkip) == 4:
        ipok = True
        for byte in checkip:
            byte = int(byte)
            if byte > 255 or byte < 0:
                ipok = False
    if not ipok:
        return(0)
    else:
        return(1)

# Lista las direcciones IP's alquiladas y reservadas
def ListarConcesiones():
    lista = commands.getoutput("cat /var/lib/dhcp/dhcpd.leases|egrep '^lease'|egrep -o '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'|sort -u")
    lista = lista.split("\n")
    reservas = commands.getoutput("sed -n '/host/,/}/p' /etc/dhcp/dhcpd.conf|grep 'option routers'|egrep -o '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'")
    reservas = reservas.split("\n")
    print('\n Direcciones IP\'s concedidas: ')
    for ip in lista:
        print(' -%s'%ip)
    print('\n Direcciones IP\'s reservadas: ')
    for ip in reservas:
        print(' -%s'%ip)

# Comprueba si la IP pasada como parámetro está concedida
def ComprobarIP(ip):
    reservadas = commands.getoutput("sed -n '/host/,/}/p' /etc/dhcp/dhcpd.conf|grep -e 'option routers' -e 'hardware'|grep -v ^#|cut -d\" \" -f6|cut -d\";\" -f1")
    reservadas = reservadas.split("\n")
    lista = commands.getoutput("cat /var/lib/dhcp/dhcpd.leases|egrep '^lease|hardware'|egrep -o '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}|[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}'")
    lista = lista.split("\n")
    concedida = []
    posicion = 0
    for direccion in reservadas:
        if direccion == ip:
            concedida.append(direccion)
            posicion = reservadas.index(direccion)
            concedida.append(reservadas[posicion-1])
    for direccion in lista:
        if direccion == ip:
            concedida.append(direccion)
            posicion = lista.index(direccion)
            concedida.append(lista[posicion+1])
    if len(concedida) == 0:
        return(0)
    else:
        return(concedida)        

def ImprimirAyuda():
    print '''
    Descripción:
    \tinfodhcp.py es una herramienta desarrollada en python que muestra información sobre las direcciones IP's concedidas por el servidor DHCP.
    Sintaxis:
    \tinfodhcp.py [OPCION] [<DIRECCIÓN_IP>]
    Opciones:
    \t-h
    \t\tMuestra la ayuda de infodhcp.py.
    \t-l
    \t\tLista las direcciones IP's concedidas.
    \t<DIRECCIÓN_IP>
    \t\tMuestra si una dirección IP ha sido concedida, junto con la dirección MAC de su cliente.
    Ejemplo:
    \tinfodhcp.py -l
    \tinfodhcp.py 192.168.1.2
    '''
    
# ParamOK almacena si el parámetro es correcto (1) o no (0)
ParamOK = 1

# NumParam almacena el número de parámetros
NumParam = int(len(sys.argv))

# IPconcedida almacena si una dirección IP ha sido alquilada (1) o no (0)
IPconcedida = 0

# Comprobación del número de parámetros
ParamOK = ComprobarNumParam(NumParam)

# PROGRAMA PRINCIPAL
if ParamOK == 1:
    ParamOK = ComprobarTipoParam(sys.argv[1])
    if ParamOK == 1:
        ListarConcesiones()
    elif ParamOK == 2:
        IPconcedida = ComprobarIP(sys.argv[1])
        if IPconcedida != 0:
            print('\n Dirección IP (%s) concedida a (%s)'%(IPconcedida[0],IPconcedida[1]))
        else:
            print('\n Dirección IP (%s) sin utilizar.'%sys.argv[1])
    elif ParamOK == 3:
        ImprimirAyuda()
    else:
        print('ERROR: Parámetro %s no válido. Prueba con "-l", "DireccIP" o "-h"'%sys.argv[1])
else:
    if ParamOK == 0:
        print('ERROR: Se necesita uno de los dos parámetros siguientes: -l | DireccIP.')
    else:
        print('ERROR: Demasiados párametros introducidos.')
