from automata.fa.dfa import DFA
from queue import Queue
import graphviz

# # Cargar el AFD desde un archivo DOT
# dfa = DFA.from_dot_file('/ruta/al/AFDfinal.dot')


# def minimize_automaton(dfa):
#     # Obtener el conjunto de estados del AFD
#     Q = dfa.states
    
#     # Obtener el alfabeto del AFD
#     sigma = dfa.alphabet
    
#     # Obtener el estado inicial del AFD
#     q0 = dfa.start_state
    
#     # Obtener el conjunto de estados de aceptación del AFD
#     F = dfa.final_states
    
#     # Paso 1: separar los estados de aceptación del resto
#     P = [F, Q-F]
    
#     # Paso 2: procesar cada clase de equivalencia
#     W = Queue()
#     for a in sigma:
#         W.put((P, a))
#     while not W.empty():
#         (A, a) = W.get()
#         X = []
#         for B in A:
#             X.append(B.intersection(dfa.transitions[B, a]))
#             X.append(B.difference(dfa.transitions[B, a]))
#         for Y in X:
#             if len(Y) > 0 and len(Y) < len(A):
#                 P.remove(A)
#                 P.extend([B for B in X if len(B) > 0])
#                 for b in sigma:
#                     W.put((X, b))
#                 break
    
#     # Paso 3: construir el AFD minimizado
#     delta = {}
#     for B in P:
#         for a in sigma:
#             for C in P:
#                 if C == B.intersection(dfa.transitions[B, a]):
#                     delta[B, a] = C
#                     break
#     q0_min = None
#     F_min = []
#     for B in P:
#         if q0 in B:
#             q0_min = B
#         if B.intersection(F):
#             F_min.append(B)
#     min_dfa = DFA(sigma, P, delta, q0_min, F_min)
    
#     return min_dfa




# # Minimizar el AFD
# min_dfa = minimize_automaton(dfa)

# # Guardar el AFD minimizado en un archivo DOT
# min_dot = min_dfa.to_dot()

# # Renderizar el archivo DOT con Graphviz
# graph = Source(min_dot)
# graph.render('min_dfa')

# Leer el archivo DOT y crear un objeto de grafo
graph = graphviz.Digraph()
graph.body = open('AFDfinal.dot').read()

# Obtener el diccionario de nodos y transiciones del AFD
afd_dict = {}
for edge in graph.edges(tail_head_iter='none'):
    from_node, to_node = edge + ('', )
    symbol = edge.attr['label']
    afd_dict.setdefault(from_node, {})[symbol] = to_node

# Guardar el AFD en una variable
afd = {
    'alphabet': list(set(symbol for transitions in afd_dict.values() for symbol in transitions.keys())),
    'states': list(afd_dict.keys()),
    'initial_state': graph.attr['start'],
    'accepting_states': [node for node in graph.nodes() if graph.node_attr.get(node, {}).get('shape', '') == 'doublecircle'],
    'transitions': afd_dict
}

# Mostrar el AFD guardado en la variable
print(afd)