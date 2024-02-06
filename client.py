import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextEdit
import socket
import threading

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 100, 400, 300)
        self.setWindowTitle('Client')

        self.send_button = QPushButton('Envoyer', self)
        self.send_button.setGeometry(250, 250, 100, 30)
        self.send_button.clicked.connect(self.send_data)

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(50, 250, 180, 30)

        self.message_display = QTextEdit(self)
        self.message_display.setGeometry(50, 50, 300, 180)

        # Démarre le thread pour recevoir des messages du serveur
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # Connexion initiale au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = '10.1.5.38'
        PORT = 12800
        self.client_socket.connect((HOST, PORT))

    def send_data(self):
        HOST = '10.1.5.38'
        PORT = 12800

        data = self.input_field.text()

        if data:
            try:
                if not self.client_socket:  # Vérifier si le socket client n'est pas déjà initialisé
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.connect((HOST, PORT))  # Établir la connexion avec le serveur

                self.client_socket.sendall(data.encode())
            except (socket.error, ConnectionError) as e:
                print("Erreur lors de la connexion au serveur:", e)

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    self.message_display.append(data.decode())
            except socket.error as e:
                print("Erreur lors de la réception de données:", e)
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = ClientWindow()
    client_window.show()
    sys.exit(app.exec_())
