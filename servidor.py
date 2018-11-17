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
        self.socket.send("You joined the chat room with {} ID\nWrite 'quit' to leave the room".format(self.id).encode())
        
        while True: 
            incomingMssg = self.socket.recv(1024).decode()
            while(incomingMssg.lower() != "quit"):
                with open(logFile, 'r+') as file:
                    # mutex.acquire()
                    file.write("Message by '{}' > '{}'".format(self.socket, incomingMssg))
                    # mutex.release()

                for c in clientes:
                    if self.id != c[2]:
                        c.soc.send("{} to you: > {}".format(self.socket, incomingMssg).encode())

            with open(logFile, 'r+') as file:
                file.write("'{}' has disconnected".format(self.socket))

            self.socket.send("You have been successfully disconnected".encode())
            for c in clientes[:]:
                if self.id == c[2]:
                    clientes.remove(c)
                else:
                    c.soc.send("'{}' has disconnected".format(self.socket).encode())

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

    while cont < 2:
        soc, datos = server.accept()

        c = Cliente(soc, datos, (cont + 1))
        clientes.append(c)
        c.start()

    for c in clientes:
        while c.isAlive():
            pass

    server.close()