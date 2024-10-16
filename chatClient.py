import socket
import threading
import sys
import tkinter as tk
from tkinter import scrolledtext
from myChatProtocol import MyChatProtocol


class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = False

        # Crear interfaz gráfica
        self.window = tk.Tk()
        self.window.title("Chat Cliente")

        # Instrucciones
        instructions = ("Escriba su mensaje y presione Enter para enviar un mensaje a todos.\n"
                        "Use @usuario <mensaje> para enviar un mensaje privado.\n")

        # Área de texto para mostrar mensajes del chat
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        # Mostrar las instrucciones en el área de texto al iniciar la ventana
        self.add_message(instructions)

        # Entrada de texto para escribir mensajes
        self.input_area = tk.Entry(self.window, width=50)
        self.input_area.pack(padx=10, pady=10)
        self.input_area.bind("<Return>", self.send_message_gui)  # Llamar send_message_gui cuando se presiona Enter

        # Botón para desconectar
        self.disconnect_button = tk.Button(self.window, text="Desconectar", command=self.initiate_disconnect)
        self.disconnect_button.pack(pady=5)

        # Manejar cierre de la ventana
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect(self, username):
        try:
            self.client_socket.connect((self.host, self.port))
            self.username = username
            MyChatProtocol.send_message(self.client_socket, MyChatProtocol.create_connect_message(username))
            response = MyChatProtocol.receive_message(self.client_socket)
            command, status = MyChatProtocol.decode_message(response)
            if command == "CONNECT_ACK" and status == "OK":
                self.add_message("Conectado exitosamente")
                self.window.title(f"Chat Cliente: Conectado como {self.username}")
                self.running = True
                threading.Thread(target=self.receive_messages, daemon=True).start()
                return True
            else:
                self.add_message("Conexión fallida")
                return False
        except Exception as e:
            self.add_message(f"Error al conectar: {e}")
            return False

    def initiate_disconnect(self):
        """Cierra la ventana y realiza la desconexión en segundo plano."""
        self.window.quit()  # Cerrar ventana inmediatamente
        threading.Thread(target=self.disconnect, daemon=True).start()  # Desconectar en segundo plano

    def disconnect(self):
        """Desconectar del servidor"""
        if self.running:
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
                    self.add_message(f"\nUsuarios conectados: {', '.join(users)}")

                elif command == "MESSAGE":
                    sender, content = params
                    self.add_message(f"\nMensaje de {sender}: {content}")

                elif command == "BROADCAST":
                    sender, content = params
                    self.add_message(f"\nBroadcast de {sender}: {content}")

                elif command == "ERROR":
                    error_code, error_message = params
                    self.add_message(f"\nError {error_code}: {error_message}")

            except (ConnectionResetError, ConnectionAbortedError) as e:
                # Si el servidor se desconecta
                print("Error: Conexión con el servidor perdida.")
                self.add_message("El servidor se ha desconectado.")
                self.running = False
                self.window.quit()  # Cerrar la ventana después de desconectarse

            except Exception as e:
                # Otros errores
                print(f"Error al recibir mensaje: {e}")
                self.add_message(f"Error al recibir mensaje: {e}")
                self.running = False
                self.window.quit()  # Cerrar la ventana después de un error

    def send_message_gui(self, event=None):
        message = self.input_area.get().strip()
        if message:
            if message.startswith("@"):
                parts = message.split(maxsplit=1)
                if len(parts) == 2:
                    recipient = parts[0][1:]  # Eliminar el símbolo @
                    content = parts[1]
                    self.send_message(recipient, content)
                else:
                    self.add_message("Formato incorrecto. Use @usuario <mensaje>")
            else:
                self.broadcast_message(message)
            self.input_area.delete(0, tk.END)  # Limpiar entrada

    def add_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)  # Scroll hacia abajo para ver el último mensaje

    def on_close(self):
        """Manejo seguro del cierre de la ventana"""
        self.initiate_disconnect()  # Llamar a la función de desconexión al cerrar la ventana

    def run_interface(self):
        self.window.mainloop()


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
