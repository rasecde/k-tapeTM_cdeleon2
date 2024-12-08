import sys

class MultiTapeTuringMachine:
    def __init__(self, input_file):
        #Init machine properties
        self.machine_name = None
        self.tape_count = 1
        self.tapes = []
        self.head_positions = []
        self.states = set()
        self.active_state = None
        self.transition_rules = []
        
        #Parse input
        self._load_machine_definition(input_file)
    
    def _load_machine_definition(self, filename):
        with open(filename, 'r') as file:
            #Machine Name and tape count
            header = file.readline().strip().split()
            self.machine_name = header[0]
            self.tape_count = int(header[1]) if len(header) > 1 else 1
            
            #Init tapes
            self.tapes = [list(file.readline().strip() + '_' * 100) for _ in range(self.tape_count)]
            self.head_positions = [0] * self.tape_count
            self.active_state = None
            
            #Parse transition rules
            for line in file:
                rule = line.strip().split()
                if not rule:
                    continue
                
                if self.active_state is None:
                    self.active_state = rule[0]
                
                #Make sure rule has enough elements
                required_length = 2 * self.tape_count + 3
                if len(rule) < required_length:
                    continue
                
                self.transition_rules.append(rule)
                self.states.update([rule[0], rule[self.tape_count + 1]])
    
    def _get_matching_rule(self, current_symbols):
        #Find matching state and tape symbols
        for rule in self.transition_rules:
            if rule[0] != self.active_state:
                continue
            
            #Check each tape for a match
            match_found = True
            for i in range(self.tape_count):
                if rule[i + 1] != '*' and rule[i + 1] != current_symbols[i]:
                    match_found = False
                    break
            
            if match_found:
                return rule
        
        return None
    
    def run(self, max_steps=1000, output_file="SimulationOutput.txt"):
        #Output results to file
        with open(output_file, 'w') as output:
            output.write(f"Simulation of {self.machine_name}\n")
            for step in range(max_steps):
                output.write(f"\nStep {step}:\n")
                current_symbols = []

                #Read tape symbols
                for tape_index in range(self.tape_count):
                    head_position = self.head_positions[tape_index]
                    tape = self.tapes[tape_index]
                
                    #Expand tape if head is out of bounds
                    if head_position >= len(tape):
                        tape.extend(['_'] * (head_position - len(tape) + 1))
                
                    current_symbols.append(tape[head_position])
                    output.write(f"Tape {tape_index + 1}: {''.join(tape[:head_position])} ({tape[head_position]}) {''.join(tape[head_position + 1:])}\n")
            
              #Find appropriate rule
                matching_rule = self._get_matching_rule(current_symbols)
                if not matching_rule:
                    output.write("No valid transition found. Halting.\n")
                    break
            
                #Update state
                self.active_state = matching_rule[self.tape_count + 1]
            
                #Update tape and head mvoements
                for tape_index in range(self.tape_count):
                    replacement = matching_rule[self.tape_count + 2 + tape_index]
                    if replacement != '*':
                        self.tapes[tape_index][self.head_positions[tape_index]] = replacement
                
                    movement = matching_rule[2 * self.tape_count + 2 + tape_index]
                    if movement == 'L':
                        self.head_positions[tape_index] = max(0, self.head_positions[tape_index] - 1)
                    elif movement == 'R':
                        self.head_positions[tape_index] += 1
            
                #Check for final state (halt)
                if self.active_state.startswith('qf'):
                    output.write("Final state reached. Halting.\n")
                    break
            else:
                output.write("Step limit reached. Halting.\n")


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    tm = MultiTapeTuringMachine(input_file)
    tm.run(output_file=output_file)
    print(f"Simulation complete. Output written to {output_file}")
