import socket
import threading
from .channel import Channel
from .bot import Bot

class Server:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.channels = {}
        self.bots = Bot()

    def broadcast(self, message, channel_name):
        for client in self.channels[channel_name].clients:
            client.send(message)

    def handle_client(self, client, channel_name):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.bots.process_command(message.decode('utf-8'), client)
                    self.broadcast(message, channel_name)
            except:
                self.channels[channel_name].remove_client(client)
                break

    def run(self):
        print("Server is running...")
        while True:
            client, addr = self.server.accept()
            print(f"Connected with {str(addr)}")

            # Assume the first message received from the client is the channel name
            channel_name = client.recv(1024).decode('utf-8')
            if channel_name not in self.channels:
                self.channels[channel_name] = Channel(channel_name)

            self.channels[channel_name].add_client(client)
            thread = threading.Thread(target=self.handle_client, args=(client, channel_name))
            thread.start()
