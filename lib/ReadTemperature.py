import os
import glob
import time

BASE_DIR = '/sys/bus/w1/devices/'
deviceFolder = glob.glob(BASE_DIR + '28*')[0]
deviceFile = deviceFolder + '/w1_slave'

def readTempRaw():
  f = open(deviceFile, 'r')
  lines = f.readlines()
  f.close()
  
  return lines
 
def ReadTemp():
  lines = readTempRaw()

  while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = readTempRaw()

  equalsPos = lines[1].find('t=')

  if equalsPos != -1:
      tempString = lines[1][equalsPos+2:]
      temperature = float(tempString) / 1000.0

      return temperature