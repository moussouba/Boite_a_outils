import random
import sys
import socket
import time

menu_number_selected = None  # number of menu selected by client
menu_level = 1  # menu level, use for display condition. Default 1
command = list()  # contain list of full selected number. For example: [1,2,3]
menu_items = [
    {
        "label": "INTERFACES RESEAUX",
        "child": [
            {
                "label": "Connectivité internet"
            },
            {
                "label": "Statistique interfaces réseaux"
            },
            {
                "label": "Statut interfaces réseaux"
            },
    
        ]
    },
    {
        "label": "ARP",
        "child": [
            {
                "label": "Cache ARP"
            },
            {
                "label": "Submenu 2-2"
            }
        ]
    },
    {
        "label": "Menu 3",
        "child": [
            {
                "label": "Submenu 3-1"
            },
            {
                "label": "Submenu 3-2"
            }
        ]
    }
]

SOCKET_SERVER_IP = '192.168.1.67'
SOCKET_SERVER_PORT = 8000

def welcome() -> None:
    version = "v1.0"
    design = '''
      @@@@@@@/   @@@@@@@@/    @@@@@@/   /|  
    @@          @@           @@         @@
    @@  <@@>     @@@@@@@@@   @@   /@@@  @@
    @@                   @@  @@     @@  @@
      @@@@@@\    \@@@@@@@@     @@@@@@   @@ ''' + version
    design2 = '''
    @@@@@@@@@   @@@@@@@@@  @@@@@@@@@   @@  
    @@          @@         @@          @@
    @@@@@       @@@@@@@@@  @@   @@@@   @@
    @@                 @@  @@     @@   @@
    @@@@@@@@@   @@@@@@@@@  @@@@@@@@@   @@ ''' + version

    banner = "\u001b[1;34m" + random.choice([design, design2])

    author = '''
    - YVES Mousouba
    - NABIL BENATMANE
    - FOLLY Ghislain
    '''
    desc = '''
    Boite à outils (Programmée à 100% en Python) de gestion 
    des informations et statistiques de la gestion du réseau sous Linux 
    '''
    print(banner)
    print("\nDescription: \n", desc)
    print("Auteurs: \n", author)
    menu(menu_items)

#  formatting server query param
def command_builder(selected_number: int):
    global command
    if selected_number == 0:  # delete the last command
        if menu_level > 1:
            command.pop()
        else:
            command = [0]
    else:  # add new command
        command.append(selected_number)


def select_menu_option(maxi: int) -> None:
    global menu_number_selected
    global menu_level
    try:
        menu_number_selected = int(input(f"Choix du menu {menu_level} (0-{maxi}): "))
        # input validation
        if not 0 <= menu_number_selected <= maxi:
            return select_menu_option(maxi)

        # exit the program
        if menu_level == 1 and menu_number_selected == 0:
            print("GOOD BYE 👋")
            sys.exit(-1)

        command_builder(menu_number_selected)

        # change menu level 1 -> n and n -> 1
        if menu_number_selected != 0:
            menu_level += 1
        else:
            if menu_level > 1:
                menu_level -= 1
    except ValueError:
        return select_menu_option(maxi)


def menu(items) -> None:
    menu_item_str = ''

    # build menu screen text
    for i, el in enumerate(items):
        menu_item_str += f"| ({i + 1}) {el['label']} \n"

    exit_text = "Quitter le programme" if menu_level == 1 else f"Revenir au menu {menu_level - 1}"
    menu_item_str += f"| (0) {exit_text}"

    print(f"\033[39m"
          f"\n+=============== INSTRUCTION MENU {menu_level} ==============="
          f"\n{menu_item_str} "
          f"\n+{'=' * 50}")

    select_menu_option(len(items))

    # make request
    if menu_number_selected != 0 and "child" not in items[menu_number_selected - 1]:
        server_socket_connect()
    # Display menu again or
    else:
        submenu = menu_items if menu_level == 1 else items[menu_number_selected - 1].get("child")
        menu(submenu)

def server_socket_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connexion au serveur
    sock.connect((SOCKET_SERVER_IP, SOCKET_SERVER_PORT))

    # Envoi de données
    sock.send(str(command).encode())

    # Réception de données
    data = sock.recv(1024*1500)
    print(data.decode())

    #print("Fin du client \n")
    sock.close()

def main():
    welcome()


if __name__ == '__main__':
    main()
