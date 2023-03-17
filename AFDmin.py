import copy
import time

# Función para procesar una cadena dada en el AFD
def Procesar_String(AFD, string):
    #Inicializar contador y cola
    contador = 0 
    q = [inicial]
    #Mientras la cola no está vacía, extraiga el valor inicial (el estado para evaluar)
    while q:
        valor = q.pop(0)
        estado = AFD[valor]
        # Si llegamos al final de una cadena
        # Si el estado en el que nos encontramos es final se acepta de la cadena,
        # Si no estamos en un estado final se rechaza la cadena
        if contador >= len(string):
            if valor in final:
                return True
            return False
        # Por cada estado que esta siendo evaludado,
        # si hay una transición con el carácter actual siendo procesado
        # Se imprime la transición y se agrega el estado resultante a la cola
        # Si no hay transición con el carácter actual, pasa al estado receptor
        for transicion in AFD[valor]:
            if string[contador] == transicion:
                print("desde ", valor, " hacia ", AFD[valor][transicion], " con ", transicion)
                q.append(AFD[valor][transicion])
            elif string[contador] not in AFD[valor]:
                print("desde ", valor, " pasa al estado ", string[contador])

        #Aumenta el contador para recorrer la cadena.
        contador += 1
    return False

# Función para cambiar el nombre de los estados del AFD mientras se minimiza
def Cambiar_Nombre(AFD, estado, estado_nuevo):
    # Por cada estado del AFD
    for elemento in AFD:
        # Por cada transicion 
        for letra in AFD[elemento]:
            # Si el estado que estamos renombrando es el resultado de alguna transición, cambie su nombre al nuevo estado
            if estado == AFD[elemento][letra]:
                AFD[elemento].update({letra : estado_nuevo})

# Funcion para minimizar el AFD
def minimizar(AFD):
    # Se inicializa la lista de eliminacion, AFD minimizado y se cambia la bandera
    eliminado = []
    min_AFD = copy.deepcopy(AFD)
    cambiado = True
    # Si bien hay un cambio (eliminación) en el AFD, se comparan los dos estados,
    # Si tienen las mismas transiciones, no se han eliminado
    # y ambos son definitivos o no definitivos, elimínelos del AFD_min y luego
    # Agréguelos a la lista eliminada y cambie el nombre de las transiciones con el estado eliminado al nuevo estado
    while(cambiado):
        cambiado = False
        for estado in AFD:
            for otro_estado in AFD:
                if estado != otro_estado:
                    if estado in min_AFD and otro_estado in min_AFD:
                        if min_AFD[estado] == min_AFD[otro_estado]:
                            if otro_estado in min_AFD and otro_estado not in eliminado:
                                if (otro_estado in final and estado in final) or (otro_estado not in final and estado not in final):


                                    eliminado.append(otro_estado)
                                    eliminado.append(estado)
                                    cambiado = True
                                    # Comprobar si alguno de los estados es inicial, para evitar ser borrado
                                    if estado in inicial:
                                        #print("Estado a eliminar: ", otro_estado)
                                        del min_AFD[otro_estado]
                                        Cambiar_Nombre(min_AFD, otro_estado, estado)
                                        if otro_estado in final:
                                            final.remove(otro_estado)
                                    elif otro_estado in inicial:
                                        #print("Estado a eliminar: ", estado)
                                        if estado in final:
                                            final.remove(estado)
                                        del min_AFD[estado]
                                        Cambiar_Nombre(min_AFD, estado, otro_estado)
                                    else:
                                        #print("Estado a eliminar: ", otro_estado)
                                        if otro_estado in final:
                                            final.remove(otro_estado)
                                        del min_AFD[otro_estado]
                                        Cambiar_Nombre(min_AFD, otro_estado, estado)

    return min_AFD



if __name__ == '__main__':
    t0 = time.perf_counter()
    path = 'AFD.txt'
    file = open(path, 'r')
    #Inicializar el AFD
    AFD = dict(dict())
    #Extraer todos los estados, alfabeto, estados iniciales y finales del archivo
    estados = file.readline().strip().split(",")
    alfabeto = file.readline().strip().split(",")
    inicial = file.readline().strip()
    final = file.readline().strip().split(",")
    # Se imprimen los datos del AFD inicial
    print("Datos obtenidos por parte del txt: ")
    print()
    print("Todos los Estados : ",estados)
    print("Alfabeto: ",alfabeto)
    print("Estados Iniciales: ", inicial)
    print("Estados Finales: ", final)

    # Para cada línea restante en el archivo, se obtiene la transición y los estados involucrados en la transición
    for linea in file:
        input_array = linea.strip().split(",")

        datos_transicion = input_array[1].split("=>")

        estado_original = input_array[0]
        caracteres_de_transicion = datos_transicion[0]
        estado_resultante = datos_transicion[1]

        # Si el estado original ya tiene una transición en el AFD, se agrega la nueva transición.,
        # de lo contrario, se crea el nuevo estado y su primera transición
        if estado_original in AFD:
            AFD[estado_original].update({caracteres_de_transicion: estado_resultante})
        else:
            AFD[estado_original] = {caracteres_de_transicion: estado_resultante}

    # Se imprime el AFD original
    print()
    print("AFD Original")
    print(AFD)
    print()
    # Se minimiza el AFD
    min_AFD = minimizar(AFD)
    # Se imprime la version minimizada del AFD
    print()
    print("AFD minimizado")
    print(min_AFD)
    print()
    # Imprimir estados finales e iniciales del AFD minimizado
    print("Estados finales ", final)
    print("Estados iniciales ", inicial)
    print()
    t1 = time.perf_counter()
    print('\nEl tiempo para minimizar un AFD: ',t1-t0)
    print('')
    # Evaluar una cadena ingresada por el uuario
    string = input("Ingresar la cadena a probar: ")
    # Procesar la cadena que se acaba de ingresar para ver si forma parte
    if Procesar_String(min_AFD, string):
        print("Aceptada")
    else:
        print("No Aceptada")