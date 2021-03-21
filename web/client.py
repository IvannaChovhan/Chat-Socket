from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import threading


class MyClient:
    HOST = 'localhost'
    PORT = 32000
    ADDR = (HOST, PORT)
    BUFSITZ = 512

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.bind(('', 0))
        self.client_socket.connect(self.ADDR)
        self.messages = []
        self.name = name
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        self.send_messages(name)
        self.lock = threading.Lock()

    def receive_message(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSITZ).decode('utf-8')
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break
                
    def send_messages(self, msg):
        try:
            self.client_socket.send(bytes(msg, 'utf8'))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e: 
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        messages_copy = self.messages
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnected(self):
        self.send_messages("{quit}")
