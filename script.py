import pickle

def load_pkl():
    try:
        with open('docs.pkl', 'rb') as file:
            docs = pickle.load(file)
            print("The file docs.pkl does exist")
            return docs
    except FileNotFoundError:
        docs = []
        print("The file docs.pkl doesn't exist")
        return []

pkl_content = load_pkl()
combined_content = ""
if pkl_content:
    for doc in pkl_content:
        combined_content += doc.page_content
else:
    print("No content in the pickle file.")

print(combined_content)
