from collections import deque

# Define el AFN
#ejemplo a|b
afn = {
    0: {'eps': {1,3}},
    1: {'a': {2}},
    2: {'eps': {5}},
    3: {'b': {4}},
    4: {'eps': {5}},
    5: {}

}

# Definir la función que construye el AFD
def construir_afd(afn, estado_inicial):
    # Inicializar el AFD
    afd = {}
    estados_afd = set()
    estados_afd.add(frozenset(epsilon_cierre({estado_inicial}, afn)))
    pendientes = deque()
    pendientes.append(estados_afd.pop())
    afd[frozenset(epsilon_cierre({estado_inicial}, afn))] = {}
    
    # Construir el AFD utilizando el método de subconjuntos
    while pendientes:
        estado_actual = pendientes.popleft()
        for simbolo in get_simbolos(afn):
            conjunto_transiciones = set()
            for estado in estado_actual:
                conjunto_transiciones |= afn.get(estado, {}).get(simbolo, set())
            conjunto_transiciones = epsilon_cierre(conjunto_transiciones, afn)
            if conjunto_transiciones:
                if frozenset(conjunto_transiciones) not in afd:
                    estados_afd.add(frozenset(conjunto_transiciones))
                    pendientes.append(conjunto_transiciones)
                    afd[frozenset(conjunto_transiciones)] = {}
                afd[frozenset(estado_actual)][simbolo] = frozenset(conjunto_transiciones)
    
    # Marcar los estados finales del AFD
    estados_finales = set()
    for conjunto_estados in estados_afd:
        if any(estado in conjunto_estados for estado in afn.get(estado_inicial, {}).get('eps', set())):
            estados_finales.add(conjunto_estados)
    
    return afd, estados_finales

# Definir la función que calcula el epsilon-cierre de un conjunto de estados
def epsilon_cierre(conjunto_estados, afn):
    resultado = set(conjunto_estados)
    pendientes = deque(resultado)
    while pendientes:
        estado_actual = pendientes.popleft()
        for estado_transicion in afn.get(estado_actual, {}).get('eps', set()):
            if estado_transicion not in resultado:
                resultado.add(estado_transicion)
                pendientes.append(estado_transicion)
    return resultado

# Definir la función que obtiene todos los símbolos de entrada del AFN
def get_simbolos(afn):
    simbolos = set()
    for estado in afn:
        for simbolo in afn[estado]:
            if simbolo != 'eps':
                simbolos.add(simbolo)
    return simbolos

# Construir el AFD y obtener los estados finales
afd, estados_finales = construir_afd(afn, 0)

# Imprimir el AFD resultante
print("AFD resultante:")
for estado, transiciones in afd.items():
    estado_str = ", ".join(str(e) for e in estado)
    print(f"Estado: {{{estado_str}}}")
    for simbolo, siguiente_estado in transiciones.items():
        siguiente_estado_str = ", ".join(str(e) for e in siguiente_estado)
        print(f"\t{simbolo} -> {{{siguiente_estado_str}}}")
    if estado in estados_finales:
        print("Es un estado final.")
    print()
