def InputHandler(arguments):

    if len(arguments) == 1:
        print("Se Requiere parámetros")

        return False

    listFlags = list(arguments[1][1:])
    values  = arguments[2:]

    diff = len(listFlags) - len(values)

    materials = ["A", "F"]

    # Comprobar existencia de parámetros

    enabledParams = ["t", "m"]

    for p in listFlags:
        exits = p in enabledParams

        if not exits:
            print('El parámetro "-{}" no existe'.format(p))
            return False

    # Comprobar correspondencia parámetro-valor

    if(diff >  0):
        print('Se requieren los valores para (-m, -t):')
        
        if len(values) == 0:
            missing = listFlags
        else:
            missing = listFlags[diff:]

        for p in missing:

            if p == 't':
                print('+ Temperatura (-t)')
            elif p == 'm':
                print('+ Material (-m):')
        
        return False

    # Comprobar tipo de datos

    for p in listFlags:

        value = values[listFlags.index(p)]

        if p == "t":
            
            try:
                response = float(value)
            except:
                print('-t debe ser un número')
                return False
        
        if p == "m":

            if not value.isalpha() or  len(value) != 1:
                print('\nEl valor de "-m" debe ser alfabético y contener un solo caracter:')
                return False
        
            if not value in materials:
                print('\nEl valor de "-m" no existe:')
                print(' - Agua (A).')
                print(' - Fermento (F).\n')
                return False


    return [listFlags, values]
