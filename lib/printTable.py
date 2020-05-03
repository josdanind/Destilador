import sys

def HorizontalLine(headList):
  lengthTable = len(headList)
  charactersTitles = 0

  for title in headList:
    charactersTitles += len(title)

  horizontalLine = "-"*(3*lengthTable + 1 + charactersTitles)

  return horizontalLine

def TableHead(headList):
  lengthTable = len(headList)
  charactersTitles = 0
  secondLine = ""
  data = ""
  i = 0

  for title in headList:
    charactersTitles += len(title)

    if (headList.index(title) == 0):
      secondLine += '| {} |'.format(headList[i])
    else:
      secondLine += ' {} |'.format(headList[i])

    i += 1

  topLine = "-"*(3*lengthTable + 1 + charactersTitles)

  headTable = topLine + '\n' + secondLine + '\n' + topLine

  return headTable

def printTableData(headList, values):
  dataLine = ""
  if(len(headList) < len(values)):
    print("Valores supera el número de columnas")
    sys.exit(1)

  if(len(headList) > len(values)):
    for e in range(len(values), len(headList)):
      values.append(0)

  i = 0

  for v in values:
    if i == 0:
      dataLine += '| {:{width}.{prec}f} |'.format(float(v), width=len(headList[i]), prec=2)
    else:
      dataLine += ' {:{width}.{prec}f} |'.format(float(v), width=len(headList[i]), prec=2)
    
    i += 1
    
  print(dataLine)
  print(HorizontalLine(headList))
