from collections import deque
from graphviz import Digraph


class NFA:
    def __init__(self, states, alphabet, initial_state, final_state, transitions):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_state = final_state
        self.transitions = transitions

    def epsilon_closure(self, states):
        closure = set(states)
        queue = deque(states)
        while queue:
            state = queue.popleft()
            for transition in self.transitions:
                if transition["desde"] == state and transition["=>"] == " ":
                    next_state = transition["hacia"]
                    if not isinstance(next_state, list):
                        next_state = [next_state]
                    for s in next_state:
                        if s not in closure:
                            closure.add(s)
                            queue.append(s)
        return frozenset(closure)

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            for transition in self.transitions:
                if transition["desde"] == state and transition["=>"] == symbol:
                    next_state = transition["hacia"]
                    if not isinstance(next_state, list):
                        next_state = [next_state]
                    next_states.update(next_state)
        return frozenset(next_states)

    def simulate(self, string):
        current_states = self.epsilon_closure({self.initial_state})
        for symbol in string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))
        return self.final_state in current_states


class DFA:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.transitions = transitions

    def accepts(self, string):
        current_state = self.initial_state
        for symbol in string:
            if (current_state, symbol) not in self.transitions:
                return False
            current_state = self.transitions[(current_state, symbol)]
        return current_state in self.final_states


def minimize_dfa(dfa):
    # Initialize a partition with the final and non-final states
    partition = [dfa.final_states, dfa.states - dfa.final_states]

    # Create a dictionary that maps states to their partition index
    state_partition = {}
    for i, p in enumerate(partition):
        for state in p:
            state_partition[state] = i

    # Iteratively refine the partition until it no longer changes
    changed = True
    while changed:
        changed = False
        new_partition = []
        for p in partition:
            sub_partitions = {}
            for state in p:
                transitions = {}
                for symbol in dfa.alphabet:
                    next_state = dfa.transitions.get((state, symbol))
                    if next_state is None:
                        continue
                    next_partition = state_partition[next_state]
                    if next_partition not in transitions:
                        transitions[next_partition] = set()
                    transitions[next_partition].add(symbol)
                transition_sets = frozenset(
                    (next_partition, frozenset(symbols))
                    for next_partition, symbols in transitions.items()
                )
                if transition_sets not in sub_partitions:
                    sub_partitions[transition_sets] = set()
                sub_partitions[transition_sets].add(state)
            new_partition.extend(sub_partitions.values())
        if new_partition != partition:
            partition = new_partition
            state_partition = {}
            for i, p in enumerate(partition):
                for state in p:
                    state_partition[state] = i
            changed = True

    # Create a new DFA with the minimized states and transitions
    minimized_states = set(range(len(partition)))
    minimized_initial_state = state_partition[dfa.initial_state]
    minimized_final_states = set(
        i
        for i, p in enumerate(partition)
        if any(state in dfa.final_states for state in p)
    )
    minimized_transitions = {}
    for i, p in enumerate(partition):
        for state in p:
            for symbol in dfa.alphabet:
                next_state = dfa.transitions.get((state, symbol))
                if next_state is not None:
                    next_partition = state_partition[next_state]
                    minimized_transitions[(i, symbol)] = next_partition

    minimized_dfa = DFA(
        states=minimized_states,
        alphabet=dfa.alphabet,
        initial_state=minimized_initial_state,
        final_states=minimized_final_states,
        transitions=minimized_transitions,
    )

    # Draw the minimized DFA using Graphviz
    dot = Digraph()
    dot.attr(rankdir="LR")
    dot.attr("node", shape="circle", order="out")

    for state in sorted(list(minimized_dfa.states)):
        if state in minimized_dfa.final_states:
            dot.node(str(state), shape="doublecircle")
        else:
            dot.node(str(state))
    dot.node(str(minimized_dfa.initial_state), shape="point")
    for (from_state, symbol), to_state in minimized_dfa.transitions.items():
        dot.edge(str(from_state), str(to_state), label=symbol)

    dot.render("MINIMIZE_AFD", format="png")

    return minimized_dfa


def nfa_to_dfa(nfa):
    alphabet = nfa.alphabet
    initial_state = nfa.epsilon_closure({nfa.initial_state})
    dfa_states = {initial_state}
    dfa_final_states = set()
    dfa_transitions = {}
    queue = [initial_state]
    while queue:
        state = queue.pop(0)
        for symbol in alphabet:
            next_states = nfa.epsilon_closure(frozenset(nfa.move(state, symbol)))
            if not next_states:
                continue
            if next_states not in dfa_states:
                dfa_states.add(next_states)
                queue.append(next_states)
            dfa_transitions[(state, symbol)] = next_states
        if nfa.final_state in state:
            dfa_final_states.add(state)

    # The following lines have been updated
    dfa_states = {i: state for i, state in enumerate(dfa_states)}
    dfa_initial_state = next(
        i for i, state in dfa_states.items() if state == initial_state
    )
    dfa_final_states = {
        i for i, state in dfa_states.items() if nfa.final_state in state
    }
    dfa_transitions = {
        (i, symbol): j
        for (state, symbol), next_state in dfa_transitions.items()
        for i, s in dfa_states.items()
        if state == s
        for j, ns in dfa_states.items()
        if next_state == ns
    }

    return dfa_states, dfa_initial_state, dfa_final_states, dfa_transitions

#Ingresar el
nfa = NFA(
    states={0, 1, 2, 3, 4, 5, 6, 7},
    alphabet={"a", "c", "b"},
    initial_state=0,
    final_state=7,
    transitions=[
        {'desde': 0, '=>': ' ', 'hacia': [1, 3]},
        {'desde': 1, '=>': 'a', 'hacia': [2]},
        {'desde': 2, '=>': ' ', 'hacia': [1, 3]},
        {'desde': 3, '=>': ' ', 'hacia': [4, 6]},
        {'desde': 4, '=>': 'b', 'hacia': [5]},
        {'desde': 5, '=>': ' ', 'hacia': [4, 6]},
        {'desde': 6, '=>': 'c', 'hacia': [7]}
    ],
)

# Convert the NFA to a DFA using the subset method
dfa_states, dfa_initial_state, dfa_final_states, dfa_transitions = nfa_to_dfa(nfa)

# Create the DFA object
dfa = DFA(
    states=set(dfa_states.keys()),
    alphabet=nfa.alphabet,
    initial_state=dfa_initial_state,
    final_states=dfa_final_states,
    transitions=dfa_transitions,
)

minimized_dfa = minimize_dfa(dfa)


string = "aba"
if dfa.accepts(string):
    print(f"{string} Es parte del lenguaje reconozido por el AFD.")
else:
    print(f"{string} No es parte del lenguaje reconozido por el AFD.")


# Print the states, transitions, and final states of the minimized DFA
print("States:", dfa.states)
print("Transitions:", dfa.transitions)
print("Final states:", dfa.final_states)


# Draw the minimized DFA using Graphviz
from graphviz import Digraph

dot = Digraph()
dot.attr(
    rankdir="LR"
)  # Add this line to change the direction of the graph to left-to-right
dot.attr("node", shape="circle", order="out")  # Add this line to order the states

for state in sorted(list(dfa.states)):  # Change the loop to iterate over sorted states
    if state in dfa.final_states:
        dot.node(str(state), shape="doublecircle")
    else:
        dot.node(str(state))
dot.node(str(dfa.initial_state), shape="point")
for (from_state, symbol), to_state in dfa.transitions.items():
    dot.edge(str(from_state), str(to_state), label=symbol)
dot.render("AFD", format="png")
