import sys
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

from lib.InputHandler import InputHandler
from lib.printTable import TableHead, printTableData
from lib.ReadTemperature import ReadTemp

setPoint, material = 90, 'F'

inputHandler = InputHandler(sys.argv)

if not inputHandler:
  sys.exit(1)

params, values = inputHandler

for p in params:
  if p == 't':
    setPoint = float(values[params.index(p)])
  if p == 'm':
    material = values[params.index(p)]

# controller constants
kp = 1 
ki = 0 
kd = 0

# controller external variables
output = 0
temperature = ReadTemp()

# controller variables
DELTA_TIME = 1
previousTime = currentTime = time.time()
E = Ed = Ei = lastError = 0

headList = ["setPoint", "Temperatura", "Output"]
headTable = TableHead(headList)
printTableData(headList, [setPoint, temperature])

while True:
  currentTime = time.time()
  
  dT = currentTime - previousTime

  if(dT >= DELTA_TIME):
    
    # Error
    E = setPoint - temperature

    # Error Integral
    Ei += E * dT

    # Error Derivativo
    Ed = (E - lastError)/dT

    # Output
    output = kp*E + ki*Ei + kd*Ei

    if output > 0:
      GPIO.output(11, True)
    else:
      GPIO.output(11, False)

    # Imprimiendo Resultados
    os.system("clear")
    print(headTable)
    printTableData(headList, [setPoint ,temperature, output])
    
    lastError = E
    previousTime = currentTime
