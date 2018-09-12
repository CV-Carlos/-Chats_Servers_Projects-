#!/usr/bin/python3

import urllib
import os
import signal
import Tkinter as tk
from Tkinter import Entry
import locale

pageRoot = "http://studentnet.cs.manchester.ac.uk/ugt/COMP18112/"
urlList = []
pageWidget = []
global returnActive
thereIsLinks = False
def main():
  global master
  master = tk.Tk()
  master.title('BROWSER')
  global frame
  frame = tk.Frame(master)
  frame.grid(row = 0, column = 0, sticky="nsew")
  master.grid_rowconfigure(0, weight=1)
  master.grid_columnconfigure(0, weight=1)
  global pageList
  pageList = ['page1.html','page2.html','page3.html']
  createWidgets(pageList, thereIsLinks)
  message = 'Welcome, please choose a page'
  msg = tk.Message(frame, text = message)
  msg.config(bg = 'lightblue', font=('times', 12, 'italic'))
  msg.grid(row=len(pageList) + 3, column=0, sticky='nsew')
  frame.grid_columnconfigure(0, minsize=500)
  frame.grid_columnconfigure(1, minsize=0)
  global entry_page
  entry_page = Entry(master)
  entry_page.grid(row=len(pageList) + 4, column=0, columnspan=1)
  entry_page.bind('<Return>', lambda(o):callback())
  button2 = tk.Button(master, text='Quit', width=25, command=master.destroy)
  button2.grid(row=len(pageList) + 5, column=0, columnspan=1)
  tk.mainloop()

def createWidgets(pageList, thereIsLinks):
  global page
  global page2
  for x in range(0, len(pageList)):
    xstr = str(x + 1)
    page = tk.Label(frame, text = xstr + './' + pageList[x])
    page.grid(row=x, column=0, columnspan=1, sticky='W')
    pageWidget.append(page)
  xstr = str(len(pageList)+ 1)
  page = tk.Label(frame, text = xstr + ': PLAY SNAKE!!!')
  page.grid(row=len(pageList) + 1, column=0, columnspan=1, sticky='W')
  #xstr = str(len(pageList)+ 2)
  #page2 = tk.Label(frame, text = xstr + ': Return to menu')
  #page2.grid(row=len(pageList) + 2, column=0, columnspan=1, sticky='W')
  #if thereIsLinks == False:
    #page2.grid_forget()
def callback():
  if entry_page.get() != '':
    banned = 'qwertyuiopasdfghjklzxcvbnm'
    if any(entry_page.get().startswith(x) for x in banned):
      message = 'Only numbers please!!'
      msg = tk.Message(frame, text = message)
      msg.config(bg = 'lightblue', font=('times', 12, 'italic'))
      msg.grid(row=5, column=0, sticky='nsew')
    else:
      inputPage = int(entry_page.get())
      global pageList
      pageMenu(inputPage)

def pageMenu(inputPage):
  pageNumber = inputPage
  global pageList
  if pageNumber <= len(pageList):
    url = pageRoot + pageList[pageNumber - 1]
    data = urllib.urlopen(url)
    printMethod(data)
  elif pageNumber == len(pageList) + 1:
    os.system('cd ~/COMP16212/ex1 && ./run')
'''
  elif pageNumber == len(pageList) + 2:
    for x in range(0, len(pageList)):
      pageWidget[x].grid_forget()
      pageList.pop(0)
    thereIsLinks = False
    pageList.append('page1.html')
    pageList.append('page2.html')
    pageList.append('page3.html')
    createWidgets(pageList, thereIsLinks)
'''
def printMethod(data):
  count = 0
  countLine = 1
  postFloat = 0.0
  messageBox = ''
  tokens = data.read().split()
  #Print the information that was found in the url
  startPrint = False #Start printing(ignore intial html elements )
  startCopyLink = False
  indexRange = 0
  colour = []
  linetrack = []
  for token in tokens:
    token.encode('utf8') #Used to eliminate b' by changing the format
    if token == '<a':
      startPrint = False
      startCopyLink = True
      continue
    if token == '</a>':
      messageBox = messageBox + '</em>'
      continue
    if startPrint and (token == '</title>' or token == '</h1>' or token
                       == '</p>'):
      startPrint = False
      itIsALink = False
      messageBox += '\n'
      count = 0
      countLine = countLine + 1
      continue
    if token == '<title>':
      startPrint = True
      count = count + 12
      messageBox = messageBox + 'Page title: '
      continue
    if token == '<h1>':
      startPrint = True
      count = count + 9
      messageBox = messageBox + 'HEADING: '
      continue
    if token == '<p>':
      startPrint = True
      count = count + 11
      messageBox = messageBox + 'PARAGRAPH: '
      continue
    if token == '<em>':
      messageBox = messageBox + '<em>'
      continue
    if token == '</em>':
      messageBox = messageBox + '</em>'
      continue
    if startPrint:
      count = count + len(str(token)) + 1
      messageBox = messageBox + str(token)
      messageBox = messageBox + ' '
      continue
    if startCopyLink:
      modifiedURL = token.replace('href="','').replace('">','')
      urlList.append(modifiedURL)
      global thereIsLinks
      thereIsLinks = True
      startCopyLink = False
      startPrint = True
      messageBox = messageBox + '<em>'
      continue
  textBox = tk.Text(frame, heigh=50, width=200)
  textBox.grid(row=10, column=0, sticky='nsew')
  textBox.insert('1.0', messageBox)
  countVar = tk.StringVar()
  i = 0
  while i < countLine:
    try:
      istr = str(i)
      pos = textBox.search("<em>", istr + '.0', stopindex="end",
                           count=countVar)
      pos2 = textBox.search("</em>", istr + '.0', stopindex="end",
                            count=countVar)
      textBox.tag_configure("search", background="green")
      textBox.tag_add("search", pos, pos2)
    except Exception as e:
        pass
    i = i + 1
  i = 0
  while i < countLine:
    try:
      istr = str(i)
      pos = textBox.search("<em>", istr + '.0', stopindex="end", count=countVar)
      pos2 = textBox.search("</em>", istr + '.0', stopindex="end", count=countVar)
      posFloat = float(pos)
      posFloat = posFloat + 0.04
      posFloat = str(posFloat)
      pos2 = float(pos2) + 0.01
      pos2Float = pos2 - 0.06
      pos2 = str(pos2)
      pos2Float = str(pos2Float)
      textBox.delete(pos, posFloat)
      textBox.delete(pos2Float, pos2)
    except Exception as e:
        pass
    i = i + 1
  if thereIsLinks:
    for x in range(0, len(pageList)):
      pageWidget[x].grid_forget()
      pageList.pop(0)
    page.grid_forget()
    for index in range (0, len(urlList)):
      urlList[index] = urlList[index].replace('./','')
      pageList.append(urlList[index])
    for index in range (0, len(urlList)):
      urlList.pop(0)
    createWidgets(pageList, thereIsLinks)
  elif thereIsLinks == False:
    for x in range(0, len(pageList)):
      pageWidget[x].grid_forget()
      pageList.pop(0)
      page.grid_forget()
    pageList.append('page1.html')
    pageList.append('page2.html')
    pageList.append('page3.html')
    createWidgets(pageList, thereIsLinks)
if __name__=="__main__":
   main()
