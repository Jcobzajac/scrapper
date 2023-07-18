import tiktoken
from gpt4web import generate_response

def checker(language, pkl_file):

    pkl_file =  str(pkl_file)

    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    max_amount_tokens = 4000
    prompt_in_tokens = encoding.encode(pkl_file)

    string = ""
    array = []

    for i in range(0, len(prompt_in_tokens), max_amount_tokens):
        #Create chunks based on constraints related to the size of tokens
        chunk = prompt_in_tokens[i:i + max_amount_tokens]  # Get a chunk of elements
        #Decode chunk with desired amount of tokens
        decoded_chunk = encoding.decode(chunk)
        prompt = generate_response(language, decoded_chunk)
        string += "".join(str(decoded_chunk))
        array.append(decoded_chunk)
    

    return string
