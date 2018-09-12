import Tkinter as Tk
from Tkinter import Entry
import sys
from ex3utils import Client

class chatInterface(Client):

    def onMessage():

    def __init__(self, chat, client):
        self.mainLabel = Tk.Label(client, text="THIS IS THE CLIENT " + \
        str(index))
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
