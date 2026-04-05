
import random
from time import sleep
from datetime import datetime

from webcligui_api import OperationState

startTime = datetime.now()

def getElapsedTime():
    curTime = datetime.now()
    elapsedTime = curTime - startTime
    return elapsedTime

def runOverServers(maxServers):
    numServers = random.randint(4, 25)
    while numServers < maxServers:
        yield numServers
        numServers += random.randint(4, 25)

def appendStatusLine(line):
  with open("neda_status.txt", "a") as statusFile:      
      statusFile.write(line)
    
maxServers = random.randint(100, 200)
for numServers in runOverServers(maxServers):
  sleep(random.randint(6, 8))
  appendStatusLine(f"Elapsed time: {getElapsedTime()}, handled servers: {numServers}\n")

appendStatusLine(f"Elapsed time: {getElapsedTime()}, {OperationState.FINISHED.value}\n")
