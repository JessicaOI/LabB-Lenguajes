from graphviz import Digraph
from collections import deque
from graphviz import Source

with open('resultadoAFN.txt', 'r') as file:
    content = file.read()
    afn_desc = eval(content)


def reescribir_afn(afn_desc):
    afn = {}
    for transicion in afn_desc:
        origen = transicion['desde']
        simbolo = transicion['=>']
        destinos = transicion['hacia']
        if origen not in afn:
            afn[origen] = {}
        if simbolo == " ":
            simbolo = "ϵ"
        if simbolo not in afn[origen]:
            afn[origen][simbolo] = set()
        for destino in destinos:
            if destino not in afn:
                afn[destino] = {}
            if simbolo not in afn[destino]:
                afn[destino][simbolo] = set()
            afn[origen][simbolo].add(destino)
    # Identificar nodos finales
    for nodo in afn:
        if not afn[nodo]:
            afn[nodo] = None
    return afn


# afn = reescribir_afn(afn_desc)
# print(afn)


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
        if any(estado in conjunto_estados for estado in afn.get(estado_inicial, {}).get('ϵ', set())):
            estados_finales.add(conjunto_estados)
    
    return afd, estados_finales

# Definir la función que calcula el epsilon-cierre de un conjunto de estados
def epsilon_cierre(conjunto_estados, afn):
    resultado = set(conjunto_estados)
    pendientes = deque(resultado)
    while pendientes:
        estado_actual = pendientes.popleft()
        for estado_transicion in afn.get(estado_actual, {}).get('ϵ', set()):
            if estado_transicion not in resultado:
                resultado.add(estado_transicion)
                pendientes.append(estado_transicion)
    return resultado

# Definir la función que obtiene todos los símbolos de entrada del AFN
def get_simbolos(afn):
    simbolos = set()
    for estado in afn:
        for simbolo in afn[estado]:
            if simbolo != 'ϵ':
                simbolos.add(simbolo)
    return simbolos

# Construir el AFD y obtener los estados finales
afd, estados_finales = construir_afd(reescribir_afn(afn_desc), 0)

# Graficar el AFD resultante
dot = Digraph(comment='AFD resultante')
dot.attr(rankdir='LR')
for estado, transiciones in afd.items():
    estado_str = ', '.join(str(e) for e in estado)
    if estado in estados_finales:
        dot.node(estado_str, estado_str, shape='doublecircle')
    else:
        dot.node(estado_str, estado_str)
    for simbolo, siguiente_estado in transiciones.items():
        siguiente_estado_str = ', '.join(str(e) for e in siguiente_estado)
        dot.edge(estado_str, siguiente_estado_str, label=simbolo)
# dot.render('afd_resultante.gv', view=True)
dot.render('AFDfinal', format='png')
# Exportar el AFD a un archivo de texto en formato DOT
with open('AFDfinal.txt', 'w') as file:
    file.write(dot.source)

# Crear objeto Source a partir del archivo de texto en formato DOT
src = Source.from_file('AFDfinal.txt')