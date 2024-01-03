import pandas as pd
import json
import os

DATASET_FOLDER = "dataset"
INSTRUCT_COMMAND_FILE = f'{DATASET_FOLDER}/instruct_command.json'
QUESTION_PREFIX = "Use the json definition above to generate a json with this quizz:\n"

BEGIN_TOKEN = "[INST]"
END_TOKEN = "[/INST]"
BEGIN_SYS_TOKEN = "<<SYS>>"
END_SYS_TOKEN = "<</SYS>>"


def generate_parquet_file(phase, record_count):
    # Load INSTRUCT_COMMAND from a JSON file and convert it to a JSON string
    with open(INSTRUCT_COMMAND_FILE, 'r') as file:
        json_file = json.load(file)
        instruct_command_str = json.dumps(json_file, indent=2)

    # Read questions from text files
    questions = []
    for i in range(1, record_count + 1):  # Adjust range as needed
        filename = f'{DATASET_FOLDER}/{phase}_question_{i}.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                questions.append(QUESTION_PREFIX + file.read().strip())
        else:
            questions.append(f"Question {i} not found.")

    # Read questions from text files
    outputs = []
    for i in range(1, record_count + 1):  # Adjust range as needed
        filename = f'{DATASET_FOLDER}/{phase}_output_{i}.json'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                json_file = json.load(file)
                outputs.append(json.dumps(json_file, indent=2))
        else:
            outputs.append('{"error": "not a quizz"}.')

    # Sample data (placeholders or mock data)
    data = {
        'index_record': [i + 1 for i in range(len(questions))],
        'question': questions,
        'output': outputs
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Construct 'instruction' column for each record
    df['instruction'] = df.apply(lambda row: BEGIN_TOKEN + BEGIN_SYS_TOKEN + "\n" + 
                                instruct_command_str + "\n" + 
                                END_SYS_TOKEN + "\n" +
                                row['question'] + "\n" + 
                                END_TOKEN, axis=1)

    # Construct 'instruction' column for each record
    df['output'] = df.apply(lambda row: row['output'], axis=1)

    dataset_file = f'{DATASET_FOLDER}/{phase}_data.parquet'

    # Save to Parquet file
    df.to_parquet(dataset_file)

    # To confirm, read back the Parquet file
    df_read = pd.read_parquet(dataset_file)
    print(df_read)

def count_questions(phase):
    total_question_files = 0
    for filename in os.listdir(DATASET_FOLDER):
        if filename.startswith(f"{phase}_question_") and filename.endswith(".txt"):
            total_question_files +=1
            
    return total_question_files    

generate_parquet_file(phase = "train", record_count = count_questions("train"))
generate_parquet_file(phase = "validate", record_count = count_questions("validate"))