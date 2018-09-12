#!/usr/bin/env python
from threading import Thread
import time
import Tkinter as Tk
import im
from Tkinter import Entry

class Chat(Tk.Frame):

    global server
    server = im.IMServerProxy('http://webdev.cs.manchester.ac.uk/~intozcc8/IMServer.php')
    global clientsList
    clientsList = []

    global numberClients

    def __init__(self,parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('CHAT')
        self.parent.withdraw()
        numberClients = int((server['numberClients']).strip())
        self.createClients(numberClients)

    def createClients(self, numberClients):
        client = Tk.Toplevel(self)
        client.geometry("300x500")
        numberClients = numberClients + 1
        server['numberClients'] = str(numberClients)
        createUser(self, client, numberClients)
        numberClients = numberClients + 1
        server['numberClients'] = str(numberClients)

    def readMessage(self, toplevel, index, newClientList):
      userMessage = toplevel.inputBox.get("1.0",Tk.END)
      toplevel.inputBox.delete("1.0", Tk.END)
      if len(userMessage) > 1:
        server[('messageClient' + str(x + 1)).strip()] = userMessage
        self.writeMessage(toplevel, index, newClientList)
        toplevel.messageBox.configure(state = "normal")
        toplevel.messageBox.insert(Tk.END, "You: " + userMessage + "\n")
        toplevel.messageBox.see(Tk.END)
        toplevel.messageBox.configure(state = "disabled")

    def writeMessage(self, sendTopLevel, index, newClientsList):
      for toplevel in newClientsList:
        if toplevel != sendTopLevel:
          toplevel.messageBox.configure(state = "normal")
          userMessage = server[('messageClient' + str(x + 1)).strip()]
          toplevel.messageBox.insert(Tk.END, "User: " + str(index + 1) + " message :"
                                     + userMessage.strip() + "\n")
          toplevel.messageBox.see(Tk.END)
          toplevel.messageBox.configure(state = "disabled")

    def getClientList(chat):
      return clientsList

class createUser(Tk.Toplevel):

    global clientObjectList
    clientObjectList = []

    def __init__(self, chatInstance, index):
        self.mainLabel = Tk.Label(toplevel, text="THIS IS THE CLIENT " + str(index + 1))
        self.mainLabel.pack()
        #scrollMessage = Tk.Scrollbar(clientsList[x])
        #scrollMessage.pack(side='left')
        self.messageLabel = Tk.Label(toplevel, text="Here appear the messages")
        self.messageLabel.pack()
        self.messageBox = Tk.Text(toplevel, heigh=25, width=100)
        self.messageBox.pack()
        #scrollMessage.config(command = messageBox.yview)
        #messageBox.config(yscrollcommand = scrollMessage.set)
        self.messageBox.configure(state = "disabled")
        self.messageLabel2 = Tk.Label(toplevel, text="Here you can write")
        self.messageLabel2.pack()
        self.buttonSend = Tk.Button(toplevel, text='SEND', width=5,
        command= lambda: chatInstance.readMessage(self, index, clientObjectList))
        self.buttonSend.pack(side='right')
        self.inputBox = Tk.Text(toplevel, heigh=10, width=100)
        self.inputBox.pack()


if __name__ == "__main__":
    master = Tk.Tk()
    chat = Chat(master)
    time.sleep(2)
    currentClients = int(server['numberClients'].strip())
    currentClientsList = chat.getClientList()
    while True:
      try:
          for x in range(currentClients):
            if (currentClientsList[x].winfo_exists()) == 0:
              del currentClientsList[x]
              currentClients = currentClients - 1
          if currentClients > 0:
            master.update()
          else:
            break
      except IndexError:
        continue
    server.clear()
    server['numberClients'] = 0
