from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore
PORT = 5005
NAME = 'TestChat'
class Endsession(Exception): pass

class CommandHanlder:
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
        #it needs a server as input parameter, and managed a list of session
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
    def do_logout(self, session, line):
        raise EndSession

class LoginRoom(Room):
    def add(self, session):
        Room.add(self, session)
        self.broadcast('Welcome to %s\r\n' % self.server.name)

    def unknown(self, session, cmd):
        session.push('please log in\nUse "login <nick>"\r\n')

    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.push('Please enter a name\r\n')
        elif name in self.server.users:
            session.push('The name "%s" is taken.\r\n' % name)
        else:
            session.name = name
            session.enter(self.server.main_room)

class ChatRoom(Room):
    def add(self, session):
        self.broadcast(session.name + 'has entered the room.\r\n')
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.name + 'has left the room.\r\n')
