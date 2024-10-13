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

                print("\nComando (m/b/q): ", end="", flush=True)

            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                self.running = False

    def run_interface(self):
        print("Bienvenido al cliente de chat")
        print("Comandos disponibles:")
        print("m: Enviar mensaje privado")
        print("b: Enviar mensaje broadcast")
        print("q: Salir")

        while self.running:
            try:
                command = input("\nComando (m/b/q): ").strip().lower()

                if command == 'm':
                    recipient = input("Destinatario: ").strip()
                    content = input("Mensaje: ").strip()
                    self.send_message(recipient, content)
                elif command == 'b':
                    content = input("Mensaje de broadcast: ").strip()
                    self.broadcast_message(content)
                elif command == 'q':
                    self.disconnect()
                    break
                else:
                    print("Comando no reconocido. Use m, b o q.")
            except KeyboardInterrupt:
                self.disconnect()
                break

if __name__ == "__main__":
    HOST = 'ec2-54-80-40-0.compute-1.amazonaws.com'
    PORT = 8080

    print("Bienvenido al cliente de chat")
    username = input("Por favor, ingrese su nombre de usuario: ").strip()

    client = ChatClient(HOST, PORT)
    if client.connect(username):
        client.run_interface()
    else:
        print("No se pudo conectar al servidor. Por favor, intente de nuevo más tarde.")
    
    sys.exit(0)