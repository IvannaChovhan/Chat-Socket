from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person


BUFSIZE = 512

HOST = 'localhost'
PORT = 32000
persons = []
ADDR = (HOST, PORT)
MAX_CONNECTION = 5


def broadcast(msg, name):
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_connection(person):
    client = person.client

    name = client.recv(BUFSIZE).decode("utf8")
    #name = client.name
    person.set_name(name)
    msg = bytes(f"{name}: Joined the chat ", "utf8")
    broadcast(msg, "")
    while True:
        try:
            msg = client.recv(BUFSIZE)
            
            if msg == bytes("{quit}", "utf8"):
                client.send(bytes("{quit}", "utf8"))
                client.close()
                broadcast(bytes(f"{name}: Left the chat", "utf8"), "")
                persons.remove(person)
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name + ': ')
                print(f"{name}: ", msg.decode("utf8"))
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def connection(SERVER):
    while True:
        try:
            client, addr = SERVER.accept()
            print(persons)
            #if check_unique(persons, client):
            person = Person(addr, client)
            persons.append(person)
            print(f"[Connection] {addr} Connected to server{time.time()}")
            Thread(target=client_connection, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break
    print("Server doesn't work")


# def check_unique(persons, client):
#     for person in persons:
#         if person.client.name == client.name:
#             return False
#         return True


if __name__ == "__main__":
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)
    print("[STARTED]Waiting for connection..")
    ACCEPT_THREAD = Thread(target=connection, args=(SERVER, ))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
