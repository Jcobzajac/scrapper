from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename 
from pdf_ingestor import ingestor
import os 
from gpt4web import load_pkl, generate_response, delete_docs_pkl, delete_pdf_files
import tempfile

app = Flask(__name__, static_url_path='/static')
CORS(app)  # This will enable CORS for all routes

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOAD_FOLDER = os.path.join(basedir, './pdf')
    ALLOWED_EXTENSIONS = {'pdf'}
    SESSION_TYPE = 'filesystem'

#View for error
@app.route("/error", methods=["GET","POST"])
def error():
    return render_template('error.html')

#View for uploading the files
@app.route("/", methods=["GET","POST"])
def upload():
    if request.method == 'POST':
      f = request.files['file'] #Fetch the PDF file and its name
      filename = secure_filename(f.filename)
      if filename.endswith(".pdf"):
        f.save(os.path.join(Config.UPLOAD_FOLDER, filename)) #Save file locally and trigger ingestor script
        try:
            ingestor(f"./pdf/{filename}")
            print(filename)
            return redirect(url_for('query'))
        except:
            return redirect(url_for('error'))

      else:
        return redirect(url_for('error'))
    else:
        return render_template('upload.html') 

#View for choosing the language
@app.route("/query", methods=["GET","POST"])
def query():
    if request.method == 'POST':
        data = request.form
        language = data['language'] #Retrieve language choosen by user
        pkl_content = load_pkl() #Create generator
        try:
            # Get a doc chunk
            doc_chunk = next(pkl_content)
        except StopIteration:
            # No more docs
            doc_chunk = ""
        delete_pdf_files('pdf') #Delete files in PDF directory
        delete_docs_pkl() #Delete file with .pkl extension
        response = generate_response(language, doc_chunk)
        return redirect(url_for('response', response=response))
    else:
        return render_template('query.html')


#View for showing/downloading response
@app.route('/response', methods=['GET', 'POST'])
def response():
    response = request.args.get('response')
    if isinstance(response, str):
        with open('response.txt', 'w') as file:
                file.write(response)
    if request.method == 'POST':
        return send_file('response.txt', as_attachment=True, download_name='response.txt')
    else:
        return render_template('response.html', response=response)



if __name__ == "__main__": 
    app.run(port=5000)