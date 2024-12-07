import random

def generate_random_string(length=10):
    """
    Generates a random string of given length using characters 'a', 'b', and 'c'.
    """
    return ''.join(random.choice('abc') for _ in range(length))

def create_transition_rule(tape_count):
    """
    Generates a random transition rule for the Turing Machine.
    """
    # Current state
    start_state = random.choice(['q0', 'q1', 'q2', 'q3', 'q4', 'qf0', 'qf1'])
    
    # Input symbols for each tape (or wildcard '*')
    input_symbols = [random.choice('abc*') for _ in range(tape_count)]
    
    # Next state
    next_state = random.choice(['q0', 'q1', 'q2', 'q3', 'q4', 'qf0', 'qf1'])
    
    # Replacement symbols for each tape (or wildcard '*')
    replacements = [random.choice('abc*') for _ in range(tape_count)]
    
    # Head movements ('L', 'R', or '*')
    movements = [random.choice(['L', 'R', '*']) for _ in range(tape_count)]
    
    return [start_state] + input_symbols + [next_state] + replacements + movements

def generate_turing_machine(tape_count=3, transition_count=10):
    """
    Creates a single Turing Machine definition with the specified number of tapes and transitions.
    """
    machine_name = "RandomMultiTapeTM"
    
    # Random tapes with data
    tapes = [generate_random_string(random.randint(5, 15)) + '_' * 100 for _ in range(tape_count)]
    
    # Generate transitions
    transitions = [create_transition_rule(tape_count) for _ in range(transition_count)]
    
    # Format the Turing Machine definition
    tm_definition = f"{machine_name} {tape_count}\n"
    tm_definition += "\n".join(tapes) + "\n"
    tm_definition += "\n".join(" ".join(rule) for rule in transitions)
    
    return tm_definition

def generate_test_cases(case_count=250, tape_count=3, transition_count=10, output_file="InputDefinition.txt"):
    """
    Generates multiple Turing Machine test cases and saves them to an output file.
    """
    with open(output_file, 'w') as file:
        for _ in range(case_count):
            tm_definition = generate_turing_machine(tape_count, transition_count)
            file.write(tm_definition + "\n\n")  # Separate test cases with a blank line

    print(f"Generated {case_count} Turing Machine test cases and saved to {output_file}.")

if __name__ == "__main__":
    # Customize the number of test cases, tapes, and transitions as needed
    generate_test_cases(case_count=250, tape_count=3, transition_count=10, output_file="Input Files/InputDefinition.txt")
