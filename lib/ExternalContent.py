import os.path as path

def WriteToFile(date, titles, data):
    
    fileName = date + ".dat"
    newFile = False
    tableHeader = ""
    line = ""
    
    u = 0
        
    if not path.exists(fileName):
        newFile = True
        for title in titles:
            
            if u == 0:
                tableHeader += "{}".format(title)
            else:
                tableHeader += ",{}".format(title)
    
            u += 1
        
        tableHeader += '\n'
    
    file = open(fileName, "a")
        
    i = 0
     
    for value in data:
        if i == 0:
            line += '{0:.2f}'.format(float(value))
        else:
            line += ',{0:.2f}'.format(float(value))
    
        i += 1
    
    line += '\n'
    
    if newFile:
        file.write(tableHeader)
    
    file.write(line)
    file.close()
    