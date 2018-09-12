#!/usr/bin/python3

#This code was modified to be compatible with python3
import urllib.request
import os
import signal
pageRoot = "http://studentnet.cs.manchester.ac.uk/ugt/COMP18112/"
urlList = []
pageList = ['page1.html','page2.html','page3.html']
def main():
  while True:
    print('1: ./page1.html')
    print('2: ./page2.html')
    print('3: ./page3.html')
    print('4: PLAY SNAKE!!!')
    print('5: Exit')
    pageNumber = int(input('Choose a page: '))
    if pageNumber <= 5:
      break
  if pageNumber < 4:
    with urllib.request.urlopen(pageRoot + pageList[pageNumber - 1]) as url:
      data = url.read()
      printMethod(data)
  if pageNumber == 4:
    os.system('cd ~/COMP16212/ex1 && ./run')
    main()
  if pageNumber == 5:
    os.kill(os.getppid(), signal.SIGHUP)
#This method
def printMethod(data):
  tokens = data.split()
  #Print the information that was found in the url
  startPrint = False #Start printing(ignore intial html elements )
  startCopyLink = False
  indexRange = 0
  for token in tokens:
    token = str(token,'utf-8') #Used to eliminate b' by changing the format
    if token == '<a':
      startPrint = False
      startCopyLink = True
      continue
    if token == '</a>':
      print ('\033[0;0m', end = "")
      continue
    if startPrint and (token == '</title>' or token == '</h1>' or token == '</p>'):
      startPrint = False
      itIsALink = False
      print ('')
      continue
    if token == '<title>':
      startPrint = True
      print ("Page title: ", end = "")
      continue
    if token == '<h1>':
      startPrint = True
      print ("HEADING: ", end = "")
      continue
    if token == '<p>':
      startPrint = True
      print ("PARAGRAPH: ", end = "")
      continue
    if token == '<em>':
      token = ''
      print ('\033[1m', end = "")
    if token == '</em>':
      token = ''
      print ('\033[0;0m', end = "")
    if startPrint:
      print (token, end = " ")
      continue
    if startCopyLink:
      modifiedURL = token.replace('href="','').replace('">','')
      urlList.append(modifiedURL)
      indexRange = indexRange + 1
      startCopyLink = False
      startPrint = True
      print ('\033[1m', end = "")
      continue
  while True:
    for index in range(0, indexRange):
      print((index+1), (":"), urlList[index])
    print((indexRange + 1),(': PLAY SNAKE!!!'))
    print((indexRange + 2),(': Exit'))
    urlNumber = int(input('Select a link: '))
    if urlNumber <= indexRange + 2:
      break
  for index in range(0, indexRange):
    urlList[index] = urlList[index].replace('./','')
  urlMethod(urlNumber, indexRange)

def urlMethod(urlNumber, indexRange):
  if urlNumber == indexRange + 1:
    os.system('cd ~/COMP16212/ex1 && ./run')
    main()
  if urlNumber == indexRange + 2:
    os.kill(os.getppid(), signal.SIGHUP)
  else:
    with urllib.request.urlopen(pageRoot + urlList[urlNumber-1]) as url:
      data = url.read()
    for index in range(0, indexRange):
      urlList.pop(0)
    printMethod(data)

if __name__=="__main__":
   main()
