import socket
import threading
import sys
from myChatProtocol import MyChatProtocol

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = False

    def connect(self, username):
        try:
            self.client_socket.connect((self.host, self.port))
            self.username = username
            MyChatProtocol.send_message(self.client_socket, MyChatProtocol.create_connect_message(username))
            response = MyChatProtocol.receive_message(self.client_socket)
            command, status = MyChatProtocol.decode_message(response)
            if command == "CONNECT_ACK" and status == "OK":
                print("Conectado exitosamente")
                self.running = True
                threading.Thread(target=self.receive_messages).start()
                return True
            else:
                print("Conexión fallida")
                return False
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def disconnect(self):
        self.running = False
        MyChatProtocol.send_message(self.client_socket, MyChatProtocol.create_disconnect_message())
        self.client_socket.close()
        print("Desconectado del servidor")

    def send_message(self, recipient, content):
        MyChatProtocol.send_message(self.client_socket, MyChatProtocol.create_message(recipient, content))

    def broadcast_message(self, content):
        MyChatProtocol.send_message(self.client_socket, MyChatProtocol.create_broadcast_message(content))

    def receive_messages(self):
        while self.running:
            try:
                message = MyChatProtocol.receive_message(self.client_socket)
                if not message:
                    break

                command, *params = MyChatProtocol.decode_message(message)

                if command == "USER_LIST":
                    users = params[0].split(',')
                    print("\nUsuarios conectados:", ", ".join(users))
                
                elif command == "MESSAGE":
                    sender, content = params
                    print(f"\nMensaje de {sender}: {content}")
                
                elif command == "BROADCAST":
                    sender, content = params
                    print(f"\nBroadcast de {sender}: {content}")
                
                elif command == "ERROR":
                    error_code, error_message = params
                    print(f"\nError {error_code}: {error_message}")

                print("> ", end="", flush=True)

            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                self.running = False

    def run_interface(self):
        print("Bienvenido al cliente de chat")
        print("Instrucciones:")
        print("- Escriba su mensaje y presione Enter para enviar un mensaje a todos")
        print("- Use @usuario <mensaje> para enviar un mensaje privado")
        print("- Escriba /logout para salir")

        while self.running:
            try:
                message = input("\n> ").strip()
                
                if message.lower() == "/logout":
                    self.disconnect()
                    break
                elif message.startswith("@"):
                    parts = message.split(maxsplit=1)
                    if len(parts) == 2:
                        recipient = parts[0][1:]  # Remove the @ symbol
                        content = parts[1]
                        self.send_message(recipient, content)
                    else:
                        print("Formato incorrecto. Use @usuario <mensaje>")
                else:
                    self.broadcast_message(message)
            except KeyboardInterrupt:
                self.disconnect()
                break

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8080

    print("Bienvenido al cliente de chat")
    username = input("Por favor, ingrese su nombre de usuario: ").strip()

    client = ChatClient(HOST, PORT)
    if client.connect(username):
        client.run_interface()
    else:
        print("No se pudo conectar al servidor. Por favor, intente de nuevo más tarde.")
    
    sys.exit(0)