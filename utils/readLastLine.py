data = open('050520.dat', 'r')

lines = data.readlines()[-1].replace('\n','').split(',')

try:
  number = float(lines[len(lines)-1])
except:
  number = 0

print(number)