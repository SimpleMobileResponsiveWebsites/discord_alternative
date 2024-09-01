class Bot:
    def __init__(self):
        self.commands = {
            '!hello': self.say_hello,
            '!help': self.show_help,
        }

    def process_command(self, message, client):
        if message in self.commands:
            response = self.commands[message]()
            client.send(response.encode('utf-8'))

    def say_hello(self):
        return "Hello! How can I assist you today?"

    def show_help(self):
        return "Available commands: !hello, !help"
