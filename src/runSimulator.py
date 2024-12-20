import os
import glob
import subprocess

#Paths
INPUT_FOLDER = "Input Files/"
OUTPUT_FOLDER = "Output Files/"

def ensure_folders_exist():
    #make sure folders exist
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_next_available_file(base_name, folder):
    #check for file number
    files = glob.glob(f"{folder}{base_name}[0-9]*.txt")
    numbers = [int(file[len(folder + base_name):-4]) for file in files if file[len(folder + base_name):-4].isdigit()]
    return max(numbers, default=0) + 1

def generate_test_cases(file_number):
    output_file = f"{INPUT_FOLDER}InputDefinition{file_number}.txt"
    temp_file = f"{INPUT_FOLDER}InputDefinition.txt"
    try:
        #run generator
        subprocess.run(["python3", "src/testCaseGenerator.py"], check=True)
        print(f"{temp_file} has been created with random test cases.\n")
        
        #rename
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
    #save files to appropriate folders
    new_input_file = f"{INPUT_FOLDER}InputDefinition{file_number}.txt"
    new_output_file = f"{OUTPUT_FOLDER}SimulationOutput{file_number}.txt"
    
    #Rename and move files
    os.rename(input_file, new_input_file)
    os.rename(output_file, new_output_file)
    print(f"Saved input to {new_input_file}")
    print(f"Saved output to {new_output_file}")

def main():
    ensure_folders_exist()

    file_number = get_next_available_file("InputDefinition", INPUT_FOLDER)

    if not generate_test_cases(file_number):
        return

    #Paths
    input_file = f"{INPUT_FOLDER}InputDefinition{file_number}.txt"
    output_file = f"{OUTPUT_FOLDER}SimulationOutput{file_number}.txt"

    #Run simulator w/ unique input file
    if not run_simulator(input_file, output_file):
        return

    print(f"Simulation complete. Output saved to {output_file}.")

if __name__ == "__main__":
    main()

