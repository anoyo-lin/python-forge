from asyncore import dispatcher
import asyncore
class ChatServer(dispatcher): pass
s = ChatServer()
asyncore.loop()

class chatServer(dispatcher):
    def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection attempt from', addr[0])
        #addr[0] is ip
s = chatServer()
s.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#need to dig into socket detail
s.bind('', 5005)
#host name is empty
s.listen(5)
asyncore.loop()

from asyncore import dispatcher
import socket, asyncore

PORT = 5005
class ChatServer(dispatcher):
    def __init__(self, port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection attempt from ', addr[0])

if __name__ == '__main__':
    s = ChatServer(PORT)
    try: asyncore.loop()
    except KeyboardInterrupt: pass
