import os
import openai
import datetime
import pickle
import logging
import glob

GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = os.getenv("OPENAI_API_KEY") 


def setup_logger():
    date = datetime.date.today().isoformat() # get today's date in YYYY-MM-DD format
    time = datetime.datetime.now().time().isoformat(timespec='seconds') # get current time in HH:MM:SS format
    filename = f'logs/log_{date}_{time}.txt' # file name with date and time

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Check if the log file already exists
    if not os.path.exists(filename):
        # If the log file doesn't exist, create it
        open(filename, 'w').close()

    # Create handlers
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(handler)

    return logger

def generate_response(user_query, doc_chunk):
    logger = setup_logger()
    combined_query = f"Please translate text after ':' to {user_query}:" + doc_chunk
    logger.info(f'Query: {combined_query}') # log the query

    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_query},
        ],
        temperature=0.3,
    )
    generated_response = response['choices'][0]['message']['content']
    logger.info(f'Response: {generated_response}') # log the response

    return generated_response

# Load the list of Document objects



def load_pkl():
    pkl_file = glob.glob("*.pkl")
    pkl_file = pkl_file[0]
    try:
        with open(f'{pkl_file}', 'rb') as file:
            docs = pickle.load(file)
            print("The file with .pkl does exist")
            return docs
    except FileNotFoundError:
        docs = []
        print("The file with .pkl doesn't exist")
        return []

def delete_docs_pkl():
    pkl_file = glob.glob("*.pkl")
    pkl_file = pkl_file[0]
    file_path = f'{pkl_file}'
    if os.path.exists(file_path):
        os.remove(file_path)
        return "The file docs.pkl deleted successfully"
    else:
        return "The file docs.pkl does not exist"

def delete_pdf_files(dir_path):
    directory = dir_path  # Specify the directory path
    file_names = os.listdir(directory) # Get all file names in the directory
    for file_name in file_names: # Iterate over the file names and delete each file
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

