#!/usr/bin/env python
import os
import subprocess
import sys
import im
import tempfile
from Queue import Queue, Empty
from threading import Thread
import time

server = im.IMServerProxy('http://webdev.cs.manchester.ac.uk/~intozcc8/IMServer.php')
server.clear()
def launch_entry_console(named_pipe):
    console = ['xterm', '-e'] # specify your favorite terminal
                                  # emulator here

    cmd = ['python', 'entry.py', named_pipe]
    return subprocess.Popen(console + cmd)


clientsList = []
numberClients = 0
server['numberClients'] = str(numberClients)
while numberClients < 2:
  numberClients = numberClients + 1
  dirname = tempfile.mkdtemp()
  named_pipe = os.path.join(dirname, 'named_pipe')
  os.mkfifo(named_pipe)
  server['numberClients'] = str(numberClients)
  p = launch_entry_console(named_pipe)
  time.sleep(0.2)
  clientsList.append(p)
while numberClients > 0:
  try:
    for x in range(len(clientsList)):
      if clientsList[x].poll() != None:
        clientsList.pop(x)
        numberClients = numberClients - 1
        server[('messageClient' + str(x + 1)).strip()] = ''
  except:
    pass
server.clear()
