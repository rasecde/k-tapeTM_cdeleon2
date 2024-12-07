import os
import glob
import subprocess

# Paths for folders
INPUT_FOLDER = "Input Files/"
OUTPUT_FOLDER = "Output Files/"

def ensure_folders_exist():
    """
    Ensure the designated folders for inputs and outputs exist.
    """
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_next_available_file(base_name, folder):
    """
    Determine the next available numbered file name within a folder.
    """
    files = glob.glob(f"{folder}{base_name}[0-9]*.txt")
    numbers = [int(file[len(folder + base_name):-4]) for file in files if file[len(folder + base_name):-4].isdigit()]
    return max(numbers, default=0) + 1

def generate_test_cases(file_number):
    output_file = f"{INPUT_FOLDER}InputDefinition{file_number}.txt"
    temp_file = f"{INPUT_FOLDER}InputDefinition.txt"
    try:
        # Run the generator to create InputDefinition.txt
        subprocess.run(["python3", "src/testCaseGenerator.py"], check=True)
        print(f"{temp_file} has been created with random test cases.\n")
        
        # Rename InputDefinition.txt to InputDefinition{file_number}.txt
        os.rename(temp_file, output_file)
        print(f"{output_file} has been created with random test cases.\n")
    except subprocess.CalledProcessError:
        print("Error generating test cases.")
        return False
    except FileNotFoundError:
        print(f"File {temp_file} not found.")
        return False
    return True

def run_simulator(input_file, output_file):
    try:
        subprocess.run(["python3", "src/multiTapeTMSimulator.py", input_file, output_file], check=True)
        print(f"Simulation completed successfully. Output saved to {output_file}.\n")
    except subprocess.CalledProcessError:
        print("Error running simulation.")
        return False
    return True


def save_results(input_file, output_file, file_number):
    """
    Save input and output files with unique numbered names to their designated folders.
    """
    new_input_file = f"{INPUT_FOLDER}InputDefinition{file_number}.txt"
    new_output_file = f"{OUTPUT_FOLDER}SimulationOutput{file_number}.txt"
    
    # Rename and move files to appropriate folders
    os.rename(input_file, new_input_file)
    os.rename(output_file, new_output_file)
    print(f"Saved input to {new_input_file}")
    print(f"Saved output to {new_output_file}")

def main():
    ensure_folders_exist()

    # Determine the next file number
    file_number = get_next_available_file("InputDefinition", INPUT_FOLDER)

    # Generate test cases with a unique file name
    if not generate_test_cases(file_number):
        return

    # Paths for input and output files
    input_file = f"{INPUT_FOLDER}InputDefinition{file_number}.txt"
    output_file = f"{OUTPUT_FOLDER}SimulationOutput{file_number}.txt"

    # Run simulator with the unique input file
    if not run_simulator(input_file, output_file):
        return

    print(f"Simulation complete. Output saved to {output_file}.")

if __name__ == "__main__":
    main()

