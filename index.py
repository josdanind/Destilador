import sys
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

from lib.InputHandler import InputHandler
from lib.printTable import TableHead, printTableData, adaptData
from lib.ReadTemperature import ReadTemp
from lib.ExternalContent import WriteToFile
from prettytable import PrettyTable

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
kp = 60
ki = 0.0001
kd = 20

# controller external variables
output = 0
temperature = ReadTemp()

# controller variables
DELTA_TIME = 1
previousTime = currentTime = time.time()
E = Ed = Ei = lastError = 0
DATE = time.strftime("%d%m%y")

# Tiempo Del Proceso
processTime = 0

try:
    data = open(DATE + ".dat", 'r')
    lines = data.readlines()[-1].replace('\n','').split(',')
    processTime = float(lines[len(lines)-1])*60
    data.close()
except:
    pass
    
# Definiendo tabla

Table = PrettyTable()

tableHeader = ["setPoint", "Temperatura", "Output PID", "E. Proporcional", "E. Integral", "E. Derivativo", "Tiempo"]
tableValues = [setPoint ,temperature, output, kp*E, ki*Ei, kd*Ed, (processTime/60)]

Table.field_names = tableHeader
Table.add_row(adaptData(tableHeader, tableValues))

os.system("clear")
print(Table)

Table.del_row(0)

# Imprimir Tabla


try:
    while True:
        
        currentTime = time.time()
        dT = currentTime - previousTime
        
        if(dT >= DELTA_TIME):
            temperature = ReadTemp()
            
            # Error
            E = setPoint - temperature

            # Error Integral
            Ei += E * dT

            # Error Derivativo
            Ed = (E - lastError)/dT
            
            # Output
            output = kp*E + ki*Ei + kd*Ed

            # Actuador ON/OFF
            if output > 0:
                GPIO.output(11, True)
            else:
                GPIO.output(11, False)
            
            tableValues = [setPoint ,temperature, output, kp*E, ki*Ei, kd*Ed, (processTime/60)]
            
            Table.add_row(adaptData(tableHeader, tableValues))
            
            # Imprimiendo resultados
            os.system("clear")
            print(Table)
            Table.del_row(0)
          
            # Escritura de valores
            WriteToFile(DATE, tableHeader, tableValues)
            
            lastError = E
            previousTime = currentTime
            processTime += dT
            

except KeyboardInterrupt:
    os.system("clear")
    print("\n> Adios")
    GPIO.cleanup()
