# Importar la libreria del socket
import socket
import hashlib
import threading
import time
from socket import error
from datetime import datetime
SIZE = 2048
cn = 5
FORMAT = "utf-8"
PORT = 12345
# socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
concurrent_clients = int(input("Escriba el número de clientes que desea tener: "))
prueba = int(input("Escriba el número de la prueba que esta: "))
clients = concurrent_clients


def on_create_client(id):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t1 = time.time()
    # Modificar direccion del servidor
    host = "192.168.85.1" #"192.168.85.1"  # "192.168.1.2" # server address "localhost", 9879 # Tomas: 192.168.85.1"
    port = PORT  # server port

    message = "Connecting client {}".format(id)
    s.sendto(message.encode(), (host, port))
    print("Conectado")

    # path del archivo a guardar
    filename = "ArchivosRecibidos/Cliente" + str(id) + "-Prueba-" + str(prueba)+".txt"
    # Recibo 2 cosas

    # 1. Tamaño del archivo
    n_bytes = s.recv(SIZE)
    print("Numero de bytes recibidos", n_bytes)

    # 2. El archivo recuperado por paquetes
    send_bytes = 0
    packets = 0
    file = open(filename, "wb")
    while True:
        try:
            input_data = s.recv(SIZE)
            packets += 1
        except error:
            print("Error de lectura")
            connection = False
            break
        else:
            if input_data:
                # Compatibilidad con Python 3.
                if input_data.endswith(b"Termino:200"):
                    file.write(input_data.replace(b"Termino:200", b""))
                    file.close()
                    send_bytes += len(input_data.replace(b"Termino:200", b""))
                    connection = True
                    break
                else:
                    # Almacenar datos.
                    file.write(input_data)
                    send_bytes += len(input_data)

    # Enviar mensaje de confirmacion de recibido
    s.sendto(b"Recibido", (host, port))
    t2 = time.time()
    date = datetime.now()
    date_time = date.strftime("%m-%d-%Y-%H-%M-%S")
    text = "---------------------\n"
    text += "Tamaño del archivo: " + str(n_bytes) + " Bytes" + "\n"
    text += "Conectado con el servidor: " + str((host, port)) + "\n"
    text += "El tiempo de transferencia es: " + str(t2 - t1) + " ms""\n"
    text += "La tasa de transferencia es: " + str(float(n_bytes)/(t2-t1)) + " bytes/ms""\n"
    print(text)
    with open('logs_cliente/' + 'Cliente_' + str(id) + '_' + date_time + "-log.txt", 'a') as f:
        f.write(text)

    s.close()


class ClientThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_ID = thread_id

    def run(self):
        on_create_client(self.thread_ID)


while concurrent_clients > 0:
    thread = ClientThread(concurrent_clients)
    thread.start()
    concurrent_clients = concurrent_clients - 1

