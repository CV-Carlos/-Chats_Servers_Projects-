import sys
import re
from ex3utils import Server
import copy

class GUIServer(Server):

    def onStart(self):
        print "THE SERVER HAS STARTED"

    def onConnect(self, socket):
        print "A NEW USER HAS TRY CONNECTION"
        print "CURRENT NUMBER OF USERS IS: " + str(connectedUsers)

    def onMessage(self, socket, message):
        print "A NEW MESSAGE HAS BEEN WRITTEN"
        global parameter
        (command, sep, parameter) = message.strip().partition(' ')
        print "The command: ", command
        print "The message: ", parameter
        if command == "REGISTER":
          if self.nicknameCheck(parameter):
            socket.send("ERROR\-The user name is already taken")
          else:
            socket.send("SUCESS\-User created")
            global connectedUsers
            connectedUsers = connectedUsers + 1
	    print "CURRENT NUMBER OF USERS IS: " + str(connectedUsers)
            listUsers.append(socket)
            socket._userName = parameter
        elif command == "REGISTER-COMPLETED":
             for user in listUsers:
                 message = "LIST-USERS\-" + self.getUsersList(user)
                 user.send(message)
             for user in listUsers:
                 message = "LIST-GROUP\-" + self.getGroupList()
                 user.send(message)
        elif command == "NEW-GROUP":
             listGroups.append(parameter)
             for user in listUsers:
                 message = "LIST-GROUP\-" + self.getGroupList()
                 user.send(message)
        elif re.match(r"GLOBAL:+?", command):
             for user in listUsers:
                 if user._userName != socket._userName:
                    user.send(parameter)
        elif re.match(r"GROUP:+?", command):
             for user in listUsers:
                 if user._userName != socket._userName:
                    message = "GROUP\-" + command[6:len(command)+1] +\
                    "\-" + socket._userName + "\-" + parameter
                    user.send(message)
             return True
        elif re.match(r"PRIVATE:+?", command):
          for user in listUsers:
              if user._userName == command[8:len(command)+1]:
                message = "PRIVATE\-" + socket._userName + "\-" +\
                parameter
                user.send(message)
                return True
        elif re.match(r"LEAVE-GROUP:+?", command):
            parameter = socket._userName + " " + parameter
            for user in listUsers:
                if user._userName != socket._userName:
                   message = "LEAVE-GROUP\-" + command[12:\
                   len(command)+1] + "\-" + "SERVER" + "\-" + parameter
                   user.send(message)
        elif re.match(r"JOIN-GROUP:+?", command):
            print "here"
            parameter = socket._userName + " " + parameter
            for user in listUsers:
                if user._userName != socket._userName:
                   message = "JOIN-GROUP\-" + command[11:len(command)+1] +\
                   "\-" + "SERVER" + "\-" + parameter
                   user.send(message)
            return True

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
        if socket in listUsers:
          listUsers.remove(socket)
          for user in listUsers:            
            message = "PRIVATE\-" + socket._userName + "\-" +\
            "DISCONNECTED"
            user.send(message)
            message = "LIST-USERS\-" + self.getUsersList(user)
            user.send(message)
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
            message += user._userName + "\-"
        if len(message) == 0:
          return "No users in the chat"
        else:
          message = message[:len(message)-2]
          return message

    def getGroupList(self):
        message = ""
        for group in listGroups:
            message += group + "\-"
        if len(message) == 0:
          return "No groups in the chat"
        else:
          message = message[:len(message)-2]
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
    listGroups = []
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
