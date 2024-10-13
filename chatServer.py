import socket
import threading
from myChatProtocol import MyChatProtocol

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        username = None
        while True:
            try:
                message = MyChatProtocol.receive_message(client_socket)
                if not message:
                    break

                command, *params = MyChatProtocol.decode_message(message)
                
                if command == "CONNECT":
                    username = params[0]
                    if username in self.clients:
                        MyChatProtocol.send_message(client_socket, MyChatProtocol.create_connect_ack("FAIL"))
                    else:
                        self.clients[username] = client_socket
                        MyChatProtocol.send_message(client_socket, MyChatProtocol.create_connect_ack("OK"))
                        self.broadcast_user_list()
                
                elif command == "DISCONNECT":
                    break
                
                elif command == "MESSAGE":
                    recipient, content = params
                    if recipient in self.clients:
                        MyChatProtocol.send_message(self.clients[recipient], MyChatProtocol.encode_message("MESSAGE", username, content))
                
                elif command == "BROADCAST":
                    content = params[0]
                    self.broadcast_message(username, content)

            except Exception as e:
                print(f"Error: {e}")
                break

        if username:
            del self.clients[username]
            self.broadcast_user_list()
        client_socket.close()

    def broadcast_user_list(self):
        user_list = list(self.clients.keys())
        for client in self.clients.values():
            MyChatProtocol.send_message(client, MyChatProtocol.create_user_list(user_list))

    def broadcast_message(self, sender, content):
        for client in self.clients.values():
            MyChatProtocol.send_message(client, MyChatProtocol.encode_message("BROADCAST", sender, content))




if __name__ == "__main__":

    server = ChatServer('localhost', 8080)
    threading.Thread(target=server.start).start()