from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

class TuringMachine:
    def __init__(self, tape, transitions, initial_state, accept_states, molecule_map):
        self.tape = list(tape)
        self.head_position = 0
        self.state = initial_state
        self.transitions = transitions
        self.accept_states = accept_states
        self.molecule_map = molecule_map

    def step(self):
        if self.head_position < len(self.tape):
            symbol = self.tape[self.head_position]
        else:
            symbol = '_'

        key = (self.state, symbol)
        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            self.tape[self.head_position] = new_symbol
            self.state = new_state
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1
        else:
            self.state = None

    def run(self):
        while self.state is not None and self.state not in self.accept_states:
            self.step()

        if self.state in self.accept_states:
            molecule = self.molecule_map.get(self.state, "Desconocido")
            return {
                "input": ''.join(self.tape),
                "output": f"{''.join(self.tape)} = {molecule}",
                "accepted": True
            }
        else:
            return {
                "input": ''.join(self.tape),
                "output": f"Rechazado en el estado: {self.state}" if self.state else "Rechazado debido a una transición inválida.",
                "accepted": False
            }

transitions = {
    # Estados para agua (H2O) LISTO
    ('q0', 'H'): ('q1', 'H', 'R'),
    ('q1', '+'): ('q1_plus', '+', 'R'),
    ('q1_plus', 'H'): ('q2', 'H', 'R'),
    ('q2', '+'): ('q2_plus', '+', 'R'),
    ('q2_plus', 'O'): ('q_accept_H2O', 'O', 'R'),

    # Dióxido de carbono (CO2) listo
    ('q0', 'C'): ('q3', 'C', 'R'),
    ('q3', '+'): ('q3_plus', '+', 'R'),
    ('q3_plus', 'O'): ('q4', 'O', 'R'),
    ('q4', '+'): ('q4_plus', '+', 'R'),
    ('q4_plus', 'O'): ('q_accept_CO2', 'O', 'R'),

    # Metano (CH4) LISTE
    ('q3_plus', 'H'): ('q6', 'H', 'R'),
    ('q6', '+'): ('q6_plus', '+', 'R'),
    ('q6_plus', 'H'): ('q7', 'H', 'R'),
    ('q7', '+'): ('q7_plus', '+', 'R'),
    ('q7_plus', 'H'): ('q8', 'H', 'R'),
    ('q8', '+'): ('q8_plus', '+', 'R'),
    ('q8_plus', 'H'): ('q_accept_CH4', 'H', 'R'),

    # Amoníaco (NH3) READY
    ('q0', 'N'): ('q9', 'N', 'R'),
    ('q9', '+'): ('q9_plus', '+', 'R'),
    ('q9_plus', 'H'): ('q10', 'H', 'R'),
    ('q10', '+'): ('q10_plus', '+', 'R'),
    ('q10_plus', 'H'): ('q11', 'H', 'R'),
    ('q11', '+'): ('q11_plus', '+', 'R'),
    ('q11_plus', 'H'): ('q_accept_NH3', 'H', 'R'),

    # Ácido clorhídrico (HCl) listo
    ('q1_plus', 'C'): ('q20', 'C', 'R'),
    ('q20', 'l'): ('q_accept_HCl', 'l', 'R'),

    # Fluoruro de hidrógeno (HF) listo
    ('q1_plus', 'F'): ('q_accept_HF', 'F', 'R'),

    # Bromuro de hidrógeno (HBr) listo
    ('q1_plus', 'B'): ('q21', 'B', 'R'),
    ('q21', 'r'): ('q_accept_HBr', 'r', 'R'),

    # Ozono (O3) LISTO
    ('q0', 'O'): ('q16', 'O', 'R'),
    ('q16', '+'): ('q16_plus', '+', 'R'),
    ('q16_plus', 'O'): ('q17', 'O', 'R'),
    ('q17', '+'): ('q17_plus', '+', 'R'),
    ('q17_plus', 'O'): ('q_accept_O3', 'O', 'R'),

    # Sulfuro de hidrógeno (H2S) LISTO
    ('q2_plus', 'S'): ('q_accept_H2S', 'S', 'R'),
    
    # Fosfina (PH3)
    ('q0', 'P'): ('q30', 'P', 'R'),
    ('q30', '+'): ('q30_plus', '+', 'R'),
    ('q30_plus', 'H'): ('q31', 'H', 'R'),
    ('q31', '+'): ('q31_plus', '+', 'R'),
    ('q31_plus', 'H'): ('q32', 'H', 'R'),
    ('q32', '+'): ('q32_plus', '+', 'R'),
    ('q32_plus', 'H'): ('q_accept_PH3', 'H', 'R'),

    # Dióxido de nitrógeno (NO2)
    ('q0', 'N'): ('q9', 'N', 'R'),
    ('q9', '+'): ('q9_plus', '+', 'R'),
    ('q9_plus', 'O'): ('q23', 'O', 'R'),
    ('q23', '+'): ('q23_plus', '+', 'R'),
    ('q23_plus', 'O'): ('q_accept_NO2', 'O', 'R'),
    
    # Trióxido de azufre (SO3)
    ('q0', 'S'): ('q18', 'S', 'R'),
    ('q18', '+'): ('q18_plus', '+', 'R'),
    ('q18_plus', 'O'): ('q19', 'O', 'R'),
    ('q19', '+'): ('q19_plus', '+', 'R'),
    ('q19_plus', 'O'): ('q22', 'O', 'R'),
    ('q22', '+'): ('q22_plus', '+', 'R'),
    ('q22_plus', 'O'): ('q_accept_SO3', 'O', 'R'),
    
    # Óxido de dinitrógeno (N2O)
    ('q0', 'N'): ('q9', 'N', 'R'),
    ('q9', '+'): ('q9_plus', '+', 'R'),
    ('q9_plus', 'N'): ('q24', 'N', 'R'),
    ('q24', '+'): ('q24_plus', '+', 'R'),
    ('q24_plus', 'O'): ('q_accept_N2O', 'O', 'R'),
    
    
    # Óxido de hierro (Fe2O3)
    ('q0', 'F'): ('q25', 'F', 'R'),
    ('q25', 'e'): ('q26', 'e', 'R'),
    ('q26', '+'): ('q26_plus', '+', 'R'),
    ('q26_plus', 'F'): ('q27', 'F', 'R'),
    ('q27', 'e'): ('q28', 'e', 'R'),
    ('q28', '+'): ('q28_plus', '+', 'R'),
    ('q28_plus', 'O'): ('q29', 'O', 'R'),
    ('q29', '+'): ('q29_plus', '+', 'R'),
    ('q29_plus', 'O'): ('q50', 'O', 'R'),
    ('q50', '+'): ('q50_plus', '+', 'R'),
    ('q50_plus', 'O'): ('q_accept_Fe2O3', 'O', 'R'),
    
    # Óxido de aluminio (Al2O3)
    ('q0', 'A'): ('q36', 'A', 'R'),
    ('q36', 'l'): ('q37', 'l', 'R'),
    ('q37', '+'): ('q37_plus', '+', 'R'),
    ('q37_plus', 'A'): ('q38', 'A', 'R'),
    ('q38', 'l'): ('q39', 'l', 'R'),
    ('q39', '+'): ('q39_plus', '+', 'R'),
    ('q39_plus', 'O'): ('q40', 'O', 'R'),
    ('q40', '+'): ('q40_plus', '+', 'R'),
    ('q40_plus', 'O'): ('q41', 'O', 'R'),
    ('q41', '+'): ('q41_plus', '+', 'R'),
    ('q41_plus', 'O'): ('q_accept_Al2O3', 'O', 'R'),
}

molecule_map = {
'q_accept_H2O': ('H2O (Agua)'),
    'q_accept_CO2': ('CO2 (Dióxido de carbono)'),
    'q_accept_CH4': ('CH4 (Metano)'),
    'q_accept_NH3': ('NH3 (Amoníaco)'),
    'q_accept_HCl': ('HCl (Ácido clorhídrico)'),
    'q_accept_HF': ('HF (Fluoruro de hidrógeno)'),
    'q_accept_HBr': ('HBr (Bromuro de hidrógeno)'),
    'q_accept_O3': ('O3 (Ozono)'),
    'q_accept_H2S': ('H2S (Sulfuro de hidrógeno)'),
    'q_accept_PH3': ('PH3 (Fosfina)'),
    'q_accept_NO2': ('NO2 (Dióxido de nitrógeno)'),
    'q_accept_SO3': ('SO3 (Trióxido de azufre)'),
    'q_accept_N2O': ('N2O (Óxido nitroso)'),
    'q_accept_Fe2O3': ('Fe2O3 (Óxido férrico)'),
    'q_accept_Al2O3': ('Al2O3 (Óxido de aluminio)')
}

accept_states = set(molecule_map.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_tm():
    tape = request.json.get('tape', '')
    tm = TuringMachine(tape, transitions, 'q0', accept_states, molecule_map)
    result = tm.run()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
