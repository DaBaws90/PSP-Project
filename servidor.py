import socket, threading


class Cliente(threading.Thread):
    global clientes
    global mutex
    global logFile

    def __init__(self, soc, datos, id):
        super().__init__()
        self.socket = soc
        self.datos = datos
        self.id = id

    def __str__(self):
        return "Client '{}' with ID {}".format(self.datos, self.id)

    def run(self):
        print("{} connected".format(self))
        
        mutex.acquire()
        with open(logFile, 'r+') as file:
            file.write("'{}' connected".format(self))
            mutex.release()

        self.socket.send("You joined the chat room with {} ID\nWrite 'quit' to leave the room".format(self.id).encode())
        
        while True: 
            incomingMssg = self.socket.recv(1024).decode()
            while(incomingMssg.lower() != "quit"):
                mutex.acquire()
                with open(logFile, 'r+') as file:
                    # mutex.acquire()
                    file.write("Message by PC # {} > '{}'".format(self.datos, incomingMssg))
                    mutex.release()

                for c in clientes:
                    if self.id != c.id:
                        c.soc.send("{} to you: > {}".format(self.datos, incomingMssg).encode())

            mutex.acquire()
            with open(logFile, 'r+') as file:
                file.write("'{}' has disconnected".format(self.datos))
                mutex.release()

            self.socket.send("You have been successfully disconnected".encode())
            mutex.acquire()
            for c in clientes[:]:
                if self.id == c.id:
                    clientes.remove(c)
                else:
                    c.soc.send("'{}' has disconnected".format(self.datos).encode())
            mutex.release()

            break

        self.socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9999))
server.listen(10)

if __name__ == "__main__":
    clientes = []
    cont = 0
    logFile = "C:\\Users\\DaBaws-Laptop\\Desktop\\log.txt"
    mutex = threading.Lock()
    id = 1

    # while cont < 2:
    soc, datos = server.accept()

    c = Cliente(soc, datos, id)
    clientes.append(c)
    c.start()
    id += 1

    for c in clientes:
        while c.isAlive():
            pass

    server.close()
server.listen(10)

if __name__ == "__main__":
    clientes = []
    cont = 0
    logFile = "C:\\Users\\DaBaws-Laptop\\Desktop\\log.txt"
    mutex = threading.Lock()

    while cont < 2:
        soc, datos = server.accept()

        c = Cliente(soc, datos, (cont + 1))
        clientes.append(c)
        c.start()

    for c in clientes:
        while c.isAlive():
            pass

    server.close()
