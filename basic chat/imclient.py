#!/usr/bin/env python
from threading import Thread
import time
import Tkinter as Tk
import im
from Tkinter import Entry

class Chat(Tk.Frame):

    global server
    server = im.IMServerProxy('http://webdev.cs.manchester.ac.uk/' +
    '~intozcc8/IMServer.php')
    global clientsList
    clientsList = []
    chatClients = 0

    def __init__(self, parent, index):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('CHAT')
        self.parent.withdraw()
        self.createClients(index)

    def createClients(self, index):
        global client
        client = Tk.Toplevel(self)
        client.geometry("300x500")
        print index
        global user
        user = createUser(self, client, index)
        toplevel = user.getClient()

    def readMessage(self, toplevel):
      userMessage = toplevel.inputBox.get("1.0",Tk.END)
      toplevel.inputBox.delete("1.0", Tk.END)
      if len(userMessage) > 1:
        global currentClients
        server[('messageClient' + str(index)).strip()] = "User " + str(index) \
        + " message: " + userMessage
        if int(server['numberClients'][0:-2]) != int(currentClients):
          #print server['numberClients'][0:-2]
          #print currentClients
          currentClients = server['numberClients'][0:-2]
        print int(currentClients)
        for x in [i for i in range(int(currentClients)) if i != (index - 1)]:
          server[('readClient' + str(x + 1)).strip()] = \
          server[('messageClient' + str(index)).strip()]
        toplevel.messageBox.configure(state = "normal")
        toplevel.messageBox.insert(Tk.END, "You: " + userMessage + "\n")
        toplevel.messageBox.see(Tk.END)
        toplevel.messageBox.configure(state = "disabled")

    def writeMessage(self, messageWrite):
      toplevel = chat.getUser()
      toplevel.messageBox.configure(state = "normal")
      toplevel.messageBox.insert(Tk.END, messageWrite.strip() + "\n")
      toplevel.messageBox.insert(Tk.END, "\n")
      toplevel.messageBox.see(Tk.END)
      toplevel.messageBox.configure(state = "disabled")

    def getClient(self):
      return client

    def getUser(self):
      return user.getClient()

class createUser(Tk.Toplevel):

    def __init__(self, chat, client, index):
        self.mainLabel = Tk.Label(client, text="THIS IS THE CLIENT " \
        + str(index))
        self.mainLabel.pack()
        #scrollMessage = Tk.Scrollbar(clientsList[x])
        #scrollMessage.pack(side='left')
        self.messageLabel = Tk.Label(client, text="Here appear the messages")
        self.messageLabel.pack()
        self.messageBox = Tk.Text(client, heigh=25, width=100)
        self.messageBox.pack()
        #scrollMessage.config(command = messageBox.yview)
        #messageBox.config(yscrollcommand = scrollMessage.set)
        self.messageBox.configure(state = "disabled")
        self.messageLabel2 = Tk.Label(client, text="Here you can write")
        self.messageLabel2.pack()
        self.buttonSend = Tk.Button(client, text='SEND', width=5, \
        command= lambda: chat.readMessage(self))
        self.buttonSend.pack(side='right')
        self.inputBox = Tk.Text(client, heigh=10, width=100)
        self.inputBox.pack()


    def getClient(self):
      return self


if __name__ == "__main__":
    try:
      x = int(server['numberClients'].strip())
    except ValueError:
      server['numberClients'] = 0
      pass
    index = 1
    while True:
      if server[('existClient' + str(index)).strip()][0:-2] == "true":
        index = index + 1
      else:
        server[('messageClient' + str(index)).strip()] = ""
        server[('existClient' + str(index)).strip()] = "true"
        break
    currentClients = server['numberClients'][0:-2]
    print server['numberClients'][0:-2]
    currentClients = str(int(currentClients) + 1).strip()
    server['numberClients'] = currentClients
    server[('readClient' + str(index)).strip()] = ""
    master = Tk.Tk()
    chat = Chat(master, index)
    while True:
      if len(server[('readClient' + str(index)).strip()]) > 2:
              messageWrite = server[('readClient' + str(index)).strip()]
              server[('readClient' + str(index)).strip()] = ""
              chat.writeMessage(messageWrite)
      if chat.getClient().winfo_exists() == 0:
        break
      else:
        master.update()
    del server[('existClient' + str(index)).strip()]
    del server[('messageClient' + str(index)).strip()]
    del server[('readClient' + str(index)).strip()]
    currentClients = int(server['numberClients'][0:-2])
    currentClients = currentClients - 1
    server['numberClients'] = str(currentClients)
