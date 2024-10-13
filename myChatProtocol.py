import socket

class MyChatProtocol:
    ENCODING = 'utf-8'
    MAX_MESSAGE_SIZE = 1024

    @staticmethod
    def encode_message(command, *params):
        return f"{command}|{'|'.join(params)}".encode(MyChatProtocol.ENCODING)

    @staticmethod
    def decode_message(message):
        return message.decode(MyChatProtocol.ENCODING).split('|')

    @staticmethod
    def create_connect_message(username):
        return MyChatProtocol.encode_message("CONNECT", username)

    @staticmethod
    def create_disconnect_message():
        return MyChatProtocol.encode_message("DISCONNECT")

    @staticmethod
    def create_message(recipient, content):
        return MyChatProtocol.encode_message("MESSAGE", recipient, content)

    @staticmethod
    def create_broadcast_message(content):
        return MyChatProtocol.encode_message("BROADCAST", content)

    @staticmethod
    def create_connect_ack(status):
        return MyChatProtocol.encode_message("CONNECT_ACK", status)

    @staticmethod
    def create_user_list(users):
        return MyChatProtocol.encode_message("USER_LIST", ",".join(users))

    @staticmethod
    def create_error_message(error_code, error_message):
        return MyChatProtocol.encode_message("ERROR", error_code, error_message)

    @staticmethod
    def send_message(sock, message):
        sock.send(message)

    @staticmethod
    def receive_message(sock):
        return sock.recv(MyChatProtocol.MAX_MESSAGE_SIZE)