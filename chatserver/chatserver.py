#!/usr/bin/python3
from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore
PORT = 5005
NAME = 'TestChat'
class Endsession(Exception): pass

class CommandHandler:
    #it will interact with user by session
    #command_handler => room => diferent_function_room => hold_the session
    def unknown(self, session, cmd):
        session.push('Unknown command: %s\r\n' % cmd)
    def handle(self, session, line):
        #parse the line to command
        if not line.strip(): return
        #if can not separate line, it is not the command we want to parse and execute, so we return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try: line = parts[1].strip()
        except IndexError: line = ''
        #if there is no parts index 1, we assign the empty to the line
        meth = getattr(self, 'do_' + cmd, None)
        try:
            #try the command + parameter(strip or empty)
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)

class Room(CommandHandler):
    def __init__(self, server):
        #it needs a server as input parameter, and managed a list of session, EVERY SESSION NEEDS THE ONLY SERVER
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def broadcast(self, line):
        for session in self.sessions:
            session.push(line)
    #i don't understand the meaning of do_logout and it place the session and line in but only raise the endsession class. it may be can do some after work to decorate the endsession class.
    #EndSession error will trigger session.handle_close() to get into the logoutroom
    def do_logout(self, session, line):
        raise EndSession

class LoginRoom(Room):
    def add(self, session):
        Room.add(self, session)
        self.broadcast('Welcome to %s\r\n' % self.server.name)

    def unknown(self, session, cmd):
        session.push('please log in\nUse "login <nick>"\r\n')

    def do_login(self, session, line):
        name = line.strip().split('@')
        if not name[0]:
            session.push('Please enter a name\r\n')
            #a dict holds server users.
        elif name[0] in self.server.users:
            session.push('The name "%s" is taken.\r\n' % name)
        else:
            session.name = name[0]
            #ENTER TO ABSTRTACT ONLY ONE CHATROOM
            is_enter = False
            for room in self.server.main_room:
                if name[1] == room.room_name: 
                    session.enter(room)
                    is_enter = True
                    break
            if not is_enter:
                session.push('please enter correct room name, "%s" is not exists.' % name[1])
                session.push('current room_name "%s"' % name for name in room_names)

class ChatRoom(Room):
    #important
    #when a session enter a room it will call the remove/add

    def __init__(self, server, room_name):
        Room.__init__(self, server)
        self.room_name = room_name


    def add(self, session):
        self.broadcast(session.name + 'has entered the room %s.\r\n' % self.room_name)
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.name + 'has left the room %s.\r\n' % self.room_name)

    def do_say(self, session, line):
        self.broadcast(session.name + ': ' + line + '\r\n')

    def do_look(self, session, line):
        #room holds the session
        session.push('The following are in this room %s:\r\n' % self.room_name)
        for other in self.sessions:
            session.push(other.name + '\r\n')

    def do_who(self, session, line):
        #server holds the full list of connected user
        session.push('The following are logged in:\r\n')
        for name in self.server.users:
            session.push(name + '\r\n')

class LogoutRoom(Room):
    def add(self, session):
        #delete session, bind the session to user(session.name)
        try: del self.server.users[session.name]
        except KeyError: pass

#session need to server to initialize
class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator("\r\n")
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))
    def enter(self, room):
        #session attach to the abstract room of server
        #it will assume you have attribution of self.room, if not it will assign self.room = room , otherwise it will self.room.remove(self)
        try: cur = self.room
        #self.room = old room
        except AttributeError: pass
        else: cur.remove(self)
        #equal self.room.remove(self)
        self.room = room
        #attach to new room 
        room.add(self)
    def collect_incoming_data(self, data):
        self.data.appenf(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try: self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        #remove the name from self.server.names dict
        self.enter(LogoutRoom(self.server))

class ChatServer(dispatcher):
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = [ChatRoom(self, 'alpha'), ChatRoom(self, 'beta'), ChatRoom(self, 'zeta')]

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)

if __name__ == '__main__':
    s = ChatServer(PORT, NAME)
    try: asyncore.loop()
    except KeyboardInterrupt: print()
