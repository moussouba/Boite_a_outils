from ipaddress import ip_address
from os import system
import socket
import sys
import threading
import logging
import subprocess
from ping3 import ping
import psutil
from python_arptable import  get_arp_table

IP_ADDRESS = '192.168.1.67'
PORT = 8000
output = ''

# CLI color
Red = "\u001b[31m"
Green = "\u001b[32m"
Blue = "\u001b[34m"
Default = "\u001b[0m"

# config log
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='server.log')


def output_header(title='TITRE'):
    global output
    output += f"\n********************** {str(title)} **********************\n"


def job(c):
    global output
    output += f"\n ============= {str(c)} ============== \n"
    output += subprocess.check_output(["ls", "-lh"], stderr=subprocess.STDOUT, universal_newlines=True)

def arp_tables():
    global output
    output_header(title='CACHE ARP')
    d=get_arp_table()
    for element in d:
        stat = f"""
        Adresse IP : {element["IP address"]}
        Adresse MAC : {element["HW address"]}
        Interface réseau : {element["Device"]}
        Masque de sous-réseau : {element["Mask"]}

        """
        output += stat

def inet_connectivity():
    global output
    r = ping('8.8.8.8')
    output_header(title='CONNECTIVITÉ INTERNET')
    status = Green+'CONNECTED' if r else Red+'DISCONNECT'
    status += Default
    delay = f"{r * 1000:.0f} ms" if r else 'TIMEOUT'

    output += f'''
    STATUT: {status}
    DELAI: {delay}
    '''

def net_if_stats():
    global output
    d = psutil.net_io_counters(pernic=True)
    output_header(title='STATISTIQUES INTERFACES RESEAU')
    output += f"{len(d)} interface(s) réseau trouvé(s)\n"
    for i in d:
        output += f"\n{Blue}{i}:{Default}"
        stat = f"""
        {d[i][0]} octet(s) envoyé(s)
        {d[i][1]} octet(s) reçu(s)
        {d[i][2]} paquet(s) IP envoyés(s)
        {d[i][3]} paquet(s) IP reçu(s)
        {d[i][4]} paquet(s) IP entrant(s) avec erreur
        {d[i][5]} paquet(s) IP sortant(s) avec erreur
        {d[i][6]} paquet(s) IP entrant(s) abandonné(s)
        {d[i][7]} paquet(s) IP sortant(s) abandonné(s)
        """
        output += stat

def net_if_status():
    global output
    d = psutil.net_if_stats()
    output_header(title='STATUT INTERFACES RESEAU')
    output += f"{len(d)} interface(s) réseau trouvé(s)\n"
    for i in d:
        output += f"\n{Blue}{i}:{Default}"
        stat = f"""
        Etat: {Green+'Actif' if d[i][0] else Red+'Inactif'}{Default}
        Vitesse max: {d[i][2]} bps
        MTU: {d[i][3]}
        
        """
        output += stat

def exec_command(command: list):
    # reset output
    global output
    output = ''
    logging.debug(f"Command to execute: {str(command)}")
    if command:
        if command[0] == 1:  # menu 1
            if command[1] == 1:
                inet_connectivity()
            elif command[1] == 2:
                net_if_stats()
            elif command[1] == 3:
                net_if_status()
            else:
                logging.error("Error: Option unavailable")
        elif command[0] == 2:  # menu 2
            if command[1] == 1:
                arp_tables()
            elif command[1] == 2:
                job(command)
            else:
                logging.error("Error: Option unavailable")
                return None
        elif command[0] == 3:  # menu 3
            if command[1] == 1:
                print("3-1")
                job(command)
            elif command[1] == 2:
                print("3-2")
                job(command)
            else:
                logging.error("Error: Option unavailable")
                return None

        else:
            logging.error("Error: Menu unavailable")
            return None
    else:
        logging.error("Error: No command")
        return None


def createThread(c):
    try:
        # Création du Thread
        logging.debug("Thread creating...")
        t = threading.Thread(target=exec_command, args=(c,))

        # Lancement du thread
        logging.debug("Thread started...")
        t.start()

        # Attente de la fin du thread
        t.join()
        logging.debug("Thread ended...")
    except:
        logging.error("Erreur")
#net_if_addrs()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Liaison du socket Ã  une adresse et un port
sock.bind((IP_ADDRESS, PORT))

# Attente de connexion
sock.listen()

while True:
    # Acceptation de la connexion
    conn, addr = sock.accept()
    connection_info = f"{conn.getpeername()} connected"
    logging.info(connection_info)

    # Lecture dans socket
    data = conn.recv(1024*1500)

    createThread(eval(data.decode()))

    # Ecriture dans socket
    msg = f"{output}"
    conn.send(msg.encode())
    logging.info("OUTPUT sended")

# Fermeture de la connexion et du socket
conn.close()
sock.close()
