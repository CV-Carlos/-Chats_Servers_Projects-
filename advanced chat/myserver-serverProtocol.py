import sys
import re
from ex3utils import Server

class GUIServer(Server):

    def onStart(self):
        print "THE SERVER HAS STARTED"

    def onConnect(self, socket):
        print "A NEW USER HAS CONNECTED"
        global connectedUsers
        connectedUsers = connectedUsers + 1       
        socket._nameSet = False
        print "CURRENT NUMBER OF USERS IS: " + str(connectedUsers)
        socket.send("WRITE YOUR NICKNAME")

    def onMessage(self, socket, message):
        print "A NEW MESSAGE HAS BEEN WRITTEN"
        if socket._nameSet == False:
          if len(message.split()) > 1:
            socket.send("Invalid nickname, nickname must be one word length")
          else:
            if self.nicknameCheck(message):
               socket.send("Nickname already taken, choose a different one")
            else:               
               socket._userName = message.strip() 
               socket._nameSet = True
               socket.send("Welcome " + message)
               socket.send("Write 'help' to see the full list of commands")
               print "NEW NICKNAME IN THE CHAT: ", message
               listUsers.append(socket)
          return True
        global parameter
        (command, sep, parameter) = message.strip().partition(' ')
        print "The command: ", command
        print "The message: ", parameter
        if command.lower() == "global":
          for user in listUsers:
              if user._userName != socket._userName:
                user.send(parameter)
        elif re.match(r"private:+?", command.lower()):
          for user in listUsers:
              if user._userName == command[8:len(command)+1]:
                user.send(parameter)
                return True
          socket.send("User not found in the server")
        elif command.lower() == "quit":
          socket.close()
          return False
        else:
          message = self.messageProtocol(socket, command.lower())
          socket.send(message)
        return True

    def onDisconnect(self, socket):
        print "A USER HAS DISCONNECTED"
        global connectedUsers
        connectedUsers = connectedUsers - 1
        print "CURRENT NUMBER OF USERS IS: " + str(connectedUsers)

    def onStop(self):
        print "THE SERVER HAS STOPPED"

    def nicknameCheck(self,message):
        for user in listUsers:
           if user._userName.lower() == message.lower():
              return True
        return False

    def getUsersList(self, socket):
        message = ""
        for user in listUsers:
          if user._userName != socket._userName:
            message += user._userName
        if len(message) == 0:
          return "No users in the chat"
        else:
          return message

    def messageProtocol(self, socket, command):
        switch = {
                "users": self.getUsersList(socket),
                "normal": parameter,
                "upper": parameter.upper(),
                "lower": parameter.lower(),
                "capitalize":parameter.capitalize(),
                "colour": '\033[92m' + parameter + '\033[0m',
                "help": welcomeMessage
        }
        return switch.get(command, "Invalid command")


if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    connectedUsers = 0
    listUsers = []
    welcomeMessage = "COMMANDS LIST \n" +\
                    "users: Print the list of users \n" +\
                    "normal: Print the message without modifications \n" +\
                    "upper: Capitalize the full message \n" +\
                    "lower: Lowercase the full message \n" +\
                    "capitalize: Capitalize the first letter of the message\n"+\
                    "colour: Change the color of the message \n" +\
                    "global: Send a message to everybody in the server \n" +\
                    "private:'user name' Send a message to an specific user\n"+\
                    "help: Print the list of commands"
    #Start the server
    server = GUIServer()

    #Start the server with the given ip and port
    server.start(ip, port)
