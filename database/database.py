import sqlite3

class Database:
    def __init__(self, db_name='discord_app.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY,
                                channel_name TEXT NOT NULL,
                                username TEXT NOT NULL,
                                message TEXT NOT NULL)''')
        self.conn.commit()

    def add_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def save_message(self, channel_name, username, message):
        self.cursor.execute("INSERT INTO messages (channel_name, username, message) VALUES (?, ?, ?)", 
                            (channel_name, username, message))
        self.conn.commit()

    def get_messages(self, channel_name):
        self.cursor.execute("SELECT username, message FROM messages WHERE channel_name=?", (channel_name,))
        return self.cursor.fetchall()
