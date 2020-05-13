import sys
import os
import time
import RPi.GPIO as GPIO
#from IPython.display import clear_output

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

from lib.InputHandler import InputHandler
from lib.printTable import TableHead, printTableData
from lib.ReadTemperature import ReadTemp
from lib.ExternalContent import WriteToFile

setPoint, material = 97, 'F'

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
kp = 80
ki = 0.008
kd = 10

# controller external variables
output = 0
temperature = ReadTemp()

# controller variables
DELTA_TIME = 1
previousTime = currentTime = time.time()
E = Ed = Ei = lastError = 0
processTime = 0
DATE = time.strftime("%d%m%y")

headList = ["setPoint_(C)", "Temperatura_(C)", "Output", "Tiempo_(min)"]
headTable = TableHead(headList)
os.system("clear")
print(headTable)
printTableData(headList, [setPoint, temperature])

try:
    
    while True:
      currentTime = time.time()

      dT = currentTime - previousTime

      if(dT >= DELTA_TIME):
        temperature = ReadTemp()
        processTime += dT

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
        printTableData(headList, [setPoint ,temperature, output, (processTime/60)])
        
        WriteToFile(DATE, headList, [setPoint ,temperature, output, (processTime/60)])

        lastError = E
        previousTime = currentTime
        
except KeyboardInterrupt: 
    print("Adios")
    GPIO.cleanup()
