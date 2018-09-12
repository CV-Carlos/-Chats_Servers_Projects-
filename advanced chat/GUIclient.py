#!/usr/bin/env python
from threading import Thread
import time
import Tkinter as Tk
from Tkinter import Entry
import tkMessageBox
import sys
from ex3utils import Client
from time import gmtime, strftime
import Queue

class GUIclient(Client):

    def onMessage(self, socket, message):
        if message[0:10] == "LIST-USERS":
            client._onlineUsers = message[12:]
            interface.setOnlineUsers()
        elif message[0:10] == "LIST-GROUP":
            client._onlineGroups = message[12:]
            interface.setOnlineGroups()
        elif message[0:5] == "ERROR":
            interface.setClientSucess(False)
            client._errorMessage = message[7:]
        elif message[0:6] == "SUCESS":
            interface.setClientSucess(True)
        elif message[0:5] == "GROUP" or message[0:11] == "LEAVE-GROUP" or\
            message[0:10] == "JOIN-GROUP":
            command = message.split('\-', 1)[0]
            print command
            group = message.split('\-', 2)[1]
            user = message.split('\-',3)[2]
            message = message.split('\-',4)[3]
            if group in client._joinedGroupsListName:
               index = client._joinedGroupsListName.index(group)
               aGroup = client._joinedGroupsListObject[index]
               aGroup.writeMessage(user, message)
               if "withdrawn" == aGroup._group.state():
                 index = client._onlineGroupsName.index(group)
                 aGroup = client._onlineGroupsObject[index]
                 interface.flashGroup(aGroup)
            if messageBox.winfo_exists() == 1:
              if command == "LEAVE-GROUP":
                 interface.notificationModification(user + " has left the"+\
                 "group " + group)
              elif command == "JOIN-GROUP":
                 interface.notificationModification(user + " has joined the"+\
                 "group " + group)
              elif command == "GROUP":
                   interface.notificationModification("New message of: " +\
                   user + " in group:" + group)
            else:
              if command ==  "LEAVE-GROUP":
                 interface.createNotification("New message of: " + user +\
                 " in group:" + group)
              elif command ==  "JOIN-GROUP":
                   interface.notificationModification(user + " has joined the"+\
                   "group " + group)
              elif command ==  "GROUP":
                   interface.createNotification("New message of: " + user +\
                   " in group:" + group)

        elif message[0:7] == "PRIVATE":
            user = message.split('\-', 2)[1]
            message = message.split('\-',3)[2]
            if user in client._chatListName:
               index = client._chatListName.index(user)
               aChat = client._chatListObject[index]
               aChat.writeMessage(message)
               print aChat._chat.state()
               if "withdrawn" == aChat._chat.state():
                 index = client._onlineUsersName.index(user)
                 aUser = client._onlineUsersObject[index]
                 interface.flashUser(aUser)
            else:
               interface.createChat(user, None)
               index = client._chatListName.index(user)
               aChat = client._chatListObject[index]
               aChat.writeMessage(message)
               index = client._onlineUsersName.index(user)
               aUser = client._onlineUsersObject[index]
               interface.flashUser(aUser)
            if messageBox.winfo_exists() == 1:
              interface.notificationModification("New message of:" + user)
            else:
              interface.createNotification("New message of:" + user)
        return True

class clientInterface(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry("550x300")
        self.parent.title('CHAT')
        self.parent.withdraw()
        self.createClients()

    def createClients(self):
        global createUser
        createUser = Tk.Toplevel(self)
        createUser.geometry("300x200")
        createUser.ipLabel = Tk.Label(createUser, text="Introduce the ip")
        createUser.ipLabel.pack()
        createUser.ipInput = Tk.Text(createUser, heigh=2, width=100)
        createUser.ipInput.pack()
        createUser.portLabel = Tk.Label(createUser, text="Introduce the port")
        createUser.portLabel.pack()
        createUser.portInput = Tk.Text(createUser, heigh=2, width=100)
        createUser.portInput.pack()
        createUser.nameLabel = Tk.Label(createUser,\
        text="Introduce your nickname")
        createUser.nameLabel.pack()
        createUser.nameInput = Tk.Text(createUser, heigh=2, width=100)
        createUser.nameInput.pack()
        createUser.buttonEnter = Tk.Button(createUser, text='ENTER', \
        width=5, command= lambda: self.createUserHelper())
        createUser.buttonEnter.config(state = "disabled")
        createUser.buttonEnter.pack()

    def createUserHelper(self):
        try:
          ip = str(userInput.ipInput.get("1.0",Tk.END)).strip()
          port = int(str((userInput.portInput.get("1.0",Tk.END))).strip())
          global userName
          userName = str(userInput.nameInput.get("1.0",Tk.END)).strip()
          global client
          client = GUIclient()
          client.start(ip, port)
          client.send('REGISTER %s' % userName)
          global clientSucess
          clientSucess = None
          while True:
              clientSucess = self.update()
              if clientSucess == True:
                client._onlineUsersObject = []
                client._onlineUsersName = []
                client._chatListObject = []
                client._chatListName = []
                client._onlineGroupsObject = []
                client._onlineGroupsName = []
                client._groupListName = []
                client._groupListObject = []
                client._joinedGroupsListName = []
                client._joinedGroupsListObject = []
                client._notificationsList = []
                global main
                main = interface.parent
                main.title("CHAT - CLIENT: " + userName)
                varReady.set(1)
                self.createNotification("Registration completed")
                self.createGroupInterface()
                groupCreationInterface.withdraw()
                userInput.withdraw()
                main.deiconify()
                interface.mainInterface()
                client.send("REGISTER-COMPLETED")
                break
              elif clientSucess == False:
                client.stop()
                tkMessageBox.showwarning("Error", client._errorMessage,\
                parent=userInput)
                break
        except:
          tkMessageBox.showwarning("Error", "IP or Port not valid")

    def setClientSucess(self, aResult):
        global result
        result = aResult

    def update(self):
        clientSucess = result
        return clientSucess

    def mainInterface(self):
        main.usersLabel = Tk.Label(master, text = "Users Online", fg="white", \
        bg = "blue")
        main.grid_columnconfigure(1, weight=1)
        main.usersLabel.grid(row=0, column=1, padx=(15, 15), sticky="ew")
        main.groupsLabel = Tk.Label(master, text = "Groups Online", fg="white",\
        bg = "blue")
        main.grid_columnconfigure(2, weight=1)
        main.groupsLabel.grid(row=0, column=2, padx=(15, 15), sticky="we")
        main.buttonGroup = Tk.Button(main, text='NEW GROUP', \
        width=10, command= lambda: groupCreationInterface.deiconify())
        main.grid_columnconfigure(3, weight=1)
        main.buttonGroup.grid(row=0, column=3, padx=(15, 15), sticky="we")

    def setOnlineUsers(self):
        for user in client._onlineUsersObject:
           user.destroy()
        x = 0
        client._onlineUsersObject[:] = []
        tempList = []
        if client._onlineUsers == "No users in the chat":
           if messageBox.winfo_exists() == 1:
              self.notificationModification("No users in the chat")
           else:
              self.createNotification("No users in the chat")
        else:
            for user in client._onlineUsers.split("\-"):
               if user in client._onlineUsersName:
                  action = "Do nothing"
               else:
                  if messageBox.winfo_exists() == 1:
                     self.notificationModification("User " + user + "is online")
                  else:
                     self.createNotification("User " + user + "is online")
               x = x + 1
               main.buttonUser= Tk.Button(main, text=user.split(), width=20, \
               command= lambda aUser=user, button=(x-1):\
               self.createChat(aUser, button))
               global orig_color
               orig_color = main.buttonUser.cget("background")
               main.buttonUser.grid(row=x, column=1, padx=(30, 30), sticky="we")
               client._onlineUsersObject.append(main.buttonUser)
               tempList.append(user)
        client._onlineUsersName = tempList[:]

    def setOnlineGroups(self):
        for group in client._onlineGroupsObject:
            group.destroy()
        x = 0
        client._onlineGroupsObject[:] = []
        tempList = []
        if client._onlineGroups == "No groups in the chat":
            if messageBox.winfo_exists() == 1:
              self.notificationModification("No groups in the chat")
            else:
              self.createNotification("No groups in the chat")
        else:
            for group in client._onlineGroups.split("\-"):
               if not group in client._onlineGroupsName:
                  if messageBox.winfo_exists() == 1:
                     self.notificationModification("Group " + group + " added")
                  else:
                     self.createNotification("Group " + group + " added")
               x = x + 1
               main.buttonGroup= Tk.Button(main, text=group.split(), width=20,\
               command= lambda aGroup=group, button=(x-1):\
               self.createGroup(aGroup, button))
               global orig_color
               orig_color = main.buttonGroup.cget("background")
               main.buttonGroup.grid(row=x, column=2, padx=(30, 30),\
               sticky="we")
               client._onlineGroupsObject.append(main.buttonGroup)
               tempList.append(group)
        client._onlineGroupsName = tempList[:]

    def createNotification(self, aMessage):
        global messageBox
        messageBox = Tk.Toplevel(master)
        messageBox.title("NOTIFICATION")
        messageBox.geometry('300x50+1-1')
        messageBox.update_idletasks()
        messageBox.wm_attributes('-type', 'splash')
        messageBox.label = Tk.Label(messageBox, text="MESSAGE")
        messageBox.label.config(fon=("Ariel", 14))
        messageBox.label.pack()
        messageBox.label = Tk.Label(messageBox, text=aMessage)
        messageBox.label.config(fon=("Ariel", 12))
        messageBox.label.pack()
        client._notificationsList.append(aMessage)
        messageBox._index = len(client._notificationsList) - 1
        messageBox.previousButton = Tk.Button(messageBox, text='PREVIOUS',\
        width=10, command= lambda: self.previousNotification())
        messageBox.previousButton.pack(side = "left")
        if len(client._notificationsList) == 1:
           messageBox.previousButton.config(state = "disabled")
        messageBox.nextButton = Tk.Button(messageBox, text='NEXT',\
        width=10, command= lambda: self.nextNotification())
        messageBox.nextButton.pack(side = "right")
        if len(client._notificationsList) == 1:
           messageBox.nextButton.config(state = "disabled")
        messageBox.closeButton = Tk.Button(messageBox, text='CLOSE',\
        width=10, command= lambda: messageBox.destroy())
        messageBox.closeButton.pack()

    def previousNotification(self):
        messageBox._index = messageBox._index - 1
        if messageBox._index == 0:
           messageBox.previousButton.config(state = "disabled")
        messageBox.label.config(text=client._notificationsList[\
        messageBox._index])
        messageBox.nextButton.config(state = "normal")


    def nextNotification(self):
        messageBox._index = messageBox._index + 1
        if messageBox._index == len(client._notificationsList) - 1:
           messageBox.nextButton.config(state = "disabled")
        messageBox.label.config(text=client._notificationsList[\
        messageBox._index])
        messageBox.previousButton.config(state = "normal")

    def notificationModification(self, aMessage):
        messageBox.label.config(text=aMessage)
        client._notificationsList.append(aMessage)
        messageBox._index = messageBox._index + 1
        messageBox.previousButton.config(state = "normal")

    def getInput(self):
        return createUser

    def flashUser(self, aUser):
        aUser.configure(background="blue")
        aUser.flash()

    def flashGroup(self, aGroup):
        aGroup.configure(background="blue")
        aGroup.flash()

    def createChat(self, user, buttonUser):
        if buttonUser != None:
          client._onlineUsersObject[buttonUser].configure(background=orig_color)
        if user in client._chatListName:
          index = client._chatListName.index(user)
          aChat = client._chatListObject[index]
          aChat._chat.deiconify()
        else:
          chat = chatInterface(self, client, userName, user, buttonUser)
          client._chatListName.append(user)
          client._chatListObject.append(chat)

    def createGroup(self, groupName, buttonGroup):
        if buttonGroup != None:
          client._onlineGroupsObject[buttonGroup].configure\
          (background=orig_color)
        if groupName in client._groupListName:
          index = client._groupListName.index(groupName)
          aGroup = client._groupListObject[index]
          aGroup._group.deiconify()
        else:
          group = groupInterface(self, client, userName, groupName, buttonGroup)
          client._groupListName.append(groupName)
          client._groupListObject.append(group)

    def createGroupInterface(self):
        global groupCreationInterface
        groupCreationInterface = Tk.Toplevel(master)
        groupCreationInterface.geometry("300x100")
        groupCreationInterface.nameLabel = Tk.Label(groupCreationInterface,\
        text="Introduce the name")
        groupCreationInterface.nameLabel.pack()
        groupCreationInterface.nameInput = Tk.Text(groupCreationInterface,\
        heigh=2, width=100)
        groupCreationInterface.nameInput.pack()
        groupCreationInterface.errorLabel = Tk.Label(groupCreationInterface,\
        text="")
        groupCreationInterface.errorLabel.pack()
        groupCreationInterface.buttonEnter = Tk.Button(groupCreationInterface,\
        text='CREATE', \
        width=5, command= lambda: self.groupCreationInterfaceHelper())
        groupCreationInterface.buttonEnter.pack()
        groupCreationInterface.wm_protocol("WM_DELETE_WINDOW", lambda:\
        self.group_on_delete())

    def group_on_delete(self):
        groupCreationInterface.withdraw()

    def groupCreationInterfaceHelper(self):
        groupName = (groupCreationInterface.nameInput.get(1.0, Tk.END)).strip()
        if len(groupName) == 1:
            groupCreationInterface.errorLabel.config(text="Input the name"+\
            "of the group")
            return False
        if groupName in client._onlineGroupsName:
            groupCreationInterface.errorLabel.config(text="Group name in use,"+\
            " choose a diferent name")
            return False
        groupCreationInterface.withdraw()
        groupCreationInterface.nameInput.delete(1.0, Tk.END)
        groupCreationInterface.errorLabel.config(text="")
        group = groupInterface(self, client, userName, groupName, None)
        client._joinedGroupsListName.append(groupName)
        client._joinedGroupsListObject.append(group)
        client._groupListName.append(groupName)
        client._groupListObject.append(group)
        client.send("NEW-GROUP " + groupName.strip())
        if messageBox.winfo_exists() == 1:
           self.notificationModification("Group " + groupName + " created")
        else:
           self.createNotification("Group " + groupName + " created")

class chatInterface():

    def __init__(self, main, client, userName, user, buttonUser):
        self._user = user
        global chat
        chat = Tk.Toplevel(main)
        self._chat = chat
        if buttonUser == None:
            self._chat.withdraw()
        self._chat.userLabel = Tk.Label(self._chat, text=user)
        self._chat.userLabel.pack()
        self._chat.messageBox = Tk.Text(self._chat, heigh=25, width=40)
        self._chat.messageBox.pack()
        self._chat.messageBox.configure(state = "disabled")
        self._chat.buttonSend = Tk.Button(self._chat, text='SEND', width=5, \
        command= lambda: self.sendMessage(self._chat, client, user))
        self._chat.buttonSend.pack(side='right')
        self._chat.inputBox = Tk.Text(self._chat, heigh=10, width=35)
        self._chat.inputBox.pack()
        self._chat.wm_protocol("WM_DELETE_WINDOW", lambda: self.on_delete())

    def on_delete(self):
        self._chat.withdraw()

    def eliminateChat(self):
        client._chatListObject.remove(self)
        client._chatListName.remove(self._user)
        self._chat.userLabel.config(text=self._user + " DISCONNECTED")
        self._chat.wm_protocol("WM_DELETE_WINDOW", lambda: self._chat.destroy())

    def writeMessage(self, message):
        if message == "DISCONNECTED" and "normal" == self._chat.state():
           message = self._user + " HAS DISCONNECTED"
           self.eliminateChat()
           self._user = "SERVER"
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self._chat.messageBox.tag_configure("tag-center", justify="center")
        self._chat.messageBox.configure(state = "normal")
        self._chat.messageBox.insert(Tk.END, date + "\n", "tag-center")
        self._chat.messageBox.insert(Tk.END, self._user + ": " +\
        message.replace("/n|","\n") + "\n")
        self._chat.messageBox.insert(Tk.END, "\n")
        self._chat.messageBox.see(Tk.END)
        self._chat.messageBox.configure(state = "disabled")

    def sendMessage(self, chat, client, user):
        message = self._chat.inputBox.get("1.0",Tk.END)
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        if len(message) > 1:
          message = message.strip()
          self._chat.messageBox.tag_configure("tag-center", justify="center")
          self._chat.messageBox.configure(state = "normal")
          self._chat.messageBox.insert(Tk.END, date + "\n", "tag-center")
          self._chat.messageBox.insert(Tk.END, "You:" + message + "\n")
          self._chat.messageBox.insert(Tk.END, "\n")
          self._chat.messageBox.see(Tk.END)
          self._chat.messageBox.configure(state = "disabled")
          self._chat.inputBox.delete(1.0, Tk.END)
          message = "PRIVATE:" + user + " " + message.replace("\n","/n|")
          client.send(message)

class groupInterface():

    def __init__(self, main, client, userName, groupName, buttonGroup):
        self._groupName = groupName
        global group
        group = Tk.Toplevel(main)
        self._group = group
        self._group.grid_columnconfigure(2, weight=1)
        self._group.groupNameLabel = Tk.Label(self._group, text=groupName)
        self._group.groupNameLabel.grid(row=0, column=2, padx=(30, 30),\
        sticky="ew")
        self._group.grid_columnconfigure(1, weight=1)
        self._group.buttonJoin = Tk.Button(self._group, text="JOIN GROUP",\
        width=10,command= lambda: self.joinGroup())
        if buttonGroup == None:
           self._group.buttonJoin.configure(state = "disabled")
        self._group.buttonJoin.grid(row=1, column=1, padx=(30, 30),\
        sticky="ew")
        self._group.buttonLeave = Tk.Button(self._group, text="LEAVE GROUP",\
        width=10, command= lambda: self.leaveGroup())
        if "normal" == self._group.buttonJoin["state"]:
            self._group.buttonLeave.configure(state = "disabled")
        self._group.buttonLeave.grid(row=2, column=1, padx=(30, 30),\
        sticky="ew")
        self._group.messageBox = Tk.Text(self._group, heigh=25, width=40)
        self._group.messageBox.configure(state = "disabled")
        self._group.messageBox.grid(row=1, column=2, padx=(30, 30),\
        sticky="ew")
        self._group.grid_columnconfigure(3, weight=1)
        self._group.buttonSend = Tk.Button(self._group, text='SEND', width=5, \
        command= lambda: self.sendMessage(self._group, client, groupName))
        if "normal" == self._group.buttonJoin["state"]:
            self._group.buttonSend.config(state= "disabled")
        self._group.buttonSend.pack(side='right')
        self._group.buttonSend.grid(row=3, column=3, padx=(30, 30),\
        sticky="ew")
        self._group.inputBox = Tk.Text(self._group, heigh=10, width=35)
        self._group.inputBox.grid(row=3, column=2, padx=(30, 30), pady=(0,15),\
        sticky="ew")
        self._group.wm_protocol("WM_DELETE_WINDOW", lambda: self.on_delete())

    def on_delete(self):
        self._group.withdraw()

    def joinGroup(self):
        message = "JOIN-GROUP:" + self._groupName + " " + "HAS JOINED THE GROUP"
        client.send(message)
        client._joinedGroupsListName.append(self._groupName)
        client._joinedGroupsListObject.append(self)
        self._group.buttonJoin.configure(state = "disabled")
        self._group.buttonLeave.configure(state = "normal")
        self._group.buttonSend.config(state= "normal")

    def leaveGroup(self):
        message = "LEAVE-GROUP:" + self._groupName + " " + "HAS LEFT THE GROUP"
        client.send(message)
        client._joinedGroupsListName.remove(self._groupName)
        client._joinedGroupsListObject.remove(self)
        self._group.buttonJoin.configure(state = "normal")
        self._group.buttonLeave.configure(state = "disabled")
        self._group.buttonSend.config(state= "disabled")

    def writeMessage(self, user, message):
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self._group.messageBox.tag_configure("tag-center", justify="center")
        self._group.messageBox.configure(state = "normal")
        self._group.messageBox.insert(Tk.END, date + "\n", "tag-center")
        self._group.messageBox.insert(Tk.END, user + ": " + message + "\n")
        self._group.messageBox.insert(Tk.END, "\n")
        self._group.messageBox.see(Tk.END)
        self._group.messageBox.configure(state = "disabled")

    def sendMessage(self, group, client, groupName):
        message = self._group.inputBox.get("1.0",Tk.END)
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        if len(message) > 1:
          message = message.strip()
          self._group.messageBox.tag_configure("tag-center", justify="center")
          self._group.messageBox.configure(state = "normal")
          self._group.messageBox.insert(Tk.END, date + "\n", "tag-center")
          self._group.messageBox.insert(Tk.END, "You:" + message + "\n")
          self._group.messageBox.insert(Tk.END, "\n")
          self._group.messageBox.see(Tk.END)
          self._group.messageBox.configure(state = "disabled")
          self._group.inputBox.delete(1.0, Tk.END)
          message = "GROUP:" + self._groupName + " " + message
          client.send(message)


if __name__ == "__main__":

    master = Tk.Tk()
    #This variables help to control the register of the user
    varReady = Tk.IntVar()
    varCheck = Tk.IntVar()
    varSucess = Tk.IntVar()
    varCheck.set(3)
    interface = clientInterface(master)
    userIP = ""
    userPort = ""
    userName = ""
    userInput = interface.getInput()
    while True:
      if userInput.winfo_exists() == 1:
        userIP = userInput.ipInput.get("1.0",Tk.END)
        userPort = userInput.portInput.get("1.0",Tk.END)
        userName = userInput.nameInput.get("1.0",Tk.END)
        if len(userIP) > 1 and len(userPort) > 1 and len(userName) > 1:
          userInput.buttonEnter.config(state = "normal")
          if varReady.get() == 1:
            break
        else:
          userInput.buttonEnter.config(state = "disabled")
        master.update()
      else:
          if "withdrawn" == interface.parent.state():
              sys.exit()

    def on_closing():
        try:
          if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            client.stop()
            master.destroy()
        except:
          pass

    master.protocol("WM_DELETE_WINDOW", on_closing)
    master.mainloop()
