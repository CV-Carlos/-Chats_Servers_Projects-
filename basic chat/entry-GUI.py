#!/usr/bin/env python
import os
import subprocess
import sys
import im
import tempfile
from Queue import Queue, Empty
from threading import Thread
import time


def write():
  with open(sys.argv[1], 'w') as file:
    while True:
      try:
        for command in iter(lambda: raw_input('>>> '), ''):
          inputVariable = ''
          print >>file, command # pass the command to view window
          file.flush()
          server[('messageClient' + userNumber).strip()] = str(command)
          print 'Your message: ' + str(command) # do something with it
          #time.sleep(0.048)
          #server[('messageClient' + userNumber).strip()] = ''
      except Empty:
        pass

def read():
  while True:
    try:
        for x in range(int(server['numberClients'])):
          if x != (int(userNumber) - 1):
            if len(server[('messageClient' + str(x + 1)).strip()]) > 2:
              print
              sys.stdout.write('User ' + str(x + 1) + ' message ' + server[('messageClient'
                                                       + str(x + 1)).strip()])
              sys.stdout.write('>>> ')
              sys.stdout.flush()
              server[('messageClient' + str(x + 1)).strip()] = ''
    except ValueError:
      server['numberClients'] = str(backUp)
      continue

def openUser():
    while True:
        with open(sys.argv[1], 'r') as file:
          for line in iter(file.readline, ''):
            a = 2

server = im.IMServerProxy('http://webdev.cs.manchester.ac.uk/~intozcc8/IMServer.php')
userNumber = server['numberClients']
print 'User ' + userNumber
time.sleep(1)
t2 = Thread(target=openUser)
t2.daemon = True
t2.start()
messagePrinted = False
t1 = Thread(target=write) 
t1.daemon = True
t1.start()
backUp = server['numberClients']
t3 = Thread(target=read)
t3.daemon = True
t3.start()
t4 = Thread(target=main)
t4.daemon = True
t4.start()
while True:
  a = 1
