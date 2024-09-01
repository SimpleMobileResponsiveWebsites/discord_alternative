import socket
import threading
from .ui import UserInterface
from .audio import AudioHandler

class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.ui = UserInterface()
        self.audio_handler = AudioHandler()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.ui.display_message(message)
            except:
                print("Connection closed")
                break

    def send_message(self, message):
        self.client.send(message.encode('utf-8'))

    def run(self):
        channel_name = input("Enter channel name: ")
        self.client.send(channel_name.encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            message = input()
            self.send_message(message)
