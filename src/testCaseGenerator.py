import random

def generate_random_string(length=10):
    #generate random string using abc
    return ''.join(random.choice('abc') for _ in range(length))

def create_transition_rule(tape_count):
    #generate random transition for TM
    # Current state
    start_state = random.choice(['q0', 'q1', 'q2', 'q3', 'q4', 'qf0', 'qf1'])
    
    #Input symbols for each tape or "*"
    input_symbols = [random.choice('abc*') for _ in range(tape_count)]
    
    #Next state
    next_state = random.choice(['q0', 'q1', 'q2', 'q3', 'q4', 'qf0', 'qf1'])
    
    #Replacement symbols for each tape or "*"
    replacements = [random.choice('abc*') for _ in range(tape_count)]
    
    #Head movements L, R, or *
    movements = [random.choice(['L', 'R', '*']) for _ in range(tape_count)]
    
    return [start_state] + input_symbols + [next_state] + replacements + movements

def generate_turing_machine(tape_count=3, transition_count=10):
    #create single TM w/ specified # of tapes and transitions
    machine_name = "RandomMultiTapeTM"
    
    #Random tapes w/ data
    tapes = [generate_random_string(random.randint(5, 15)) + '_' * 100 for _ in range(tape_count)]
    
    #Generate transitions
    transitions = [create_transition_rule(tape_count) for _ in range(transition_count)]
    
    #Format TM
    tm_definition = f"{machine_name} {tape_count}\n"
    tm_definition += "\n".join(tapes) + "\n"
    tm_definition += "\n".join(" ".join(rule) for rule in transitions)
    
    return tm_definition

def generate_test_cases(case_count=250, tape_count=3, transition_count=10, output_file="InputDefinition.txt"):
    #generate multiple TM testcases and save them to output
    with open(output_file, 'w') as file:
        for _ in range(case_count):
            tm_definition = generate_turing_machine(tape_count, transition_count)
            file.write(tm_definition + "\n\n") 

    print(f"Generated {case_count} Turing Machine test cases and saved to {output_file}.")

if __name__ == "__main__":
    #default set to 250 testcases with 3 tapes and 10 transitions
    generate_test_cases(case_count=250, tape_count=3, transition_count=10, output_file="Input Files/InputDefinition.txt")
