import imp
from flask_cors import CORS
import os
from werkzeug.exceptions import BadRequestKeyError
from flask import Flask, request, jsonify
import clone
import screenshot
import mainhtml
import requests
import implement_backend
import htmledit
from bs4 import BeautifulSoup
from termcolor import colored
import implement_backend as backend
from urllib.parse import urlparse
import shutil
import clone2
import pickle
import subprocess


app = Flask(__name__)
CORS(app)

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.get_json()  # Access the JSON data sent from the frontend
    url = data.get('input')
    # url = request.json  # Assuming the request contains JSON data
    #url = request.form['myInput']
    #Open Keyword files:
    cwd = os.getcwd()
    
    folder_path = cwd+ "\\" + "keywords"
    link_var = []
    input_mail=[]
    input_pass=[]
    with open(os.path.join(folder_path, "link_keywords"), 'r', encoding='utf-8') as file:
        for line in file:
            link_var.append(line.strip())
    with open(os.path.join(folder_path, "mail_keywords"), 'r', encoding='utf-8') as file:
        for line in file:
            input_mail.append(line.strip())
    with open(os.path.join(folder_path, "password_keywords"), 'r', encoding='utf-8') as file:
        for line in file:
            input_pass.append(line.strip())
    #Linklists
    links_with_text = []


    urlpath = cwd + "\\url"
    with open (urlpath ,"w") as file:
        file.write(url)

    #Scrape Page:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        'Referer': 'https://www.example.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',  # Specify accepted encodings
        'Connection': 'keep-alive',  # Keep the connection alive
        'Cache-Control': 'max-age=0',  # Specify caching behavior
        'Upgrade-Insecure-Requests': '1',  # Signal support for upgrading to HTTPS
        'DNT': '1',  # Enable Do Not Track
        'X-Requested-With': 'XMLHttpRequest',  # Indicate AJAX request
        # Add more headers as required
    }
    result = requests.get(url, headers=headers).text
    doc = BeautifulSoup(result, "html.parser")
    with open('output.html', 'w', encoding="utf-8") as file:
        file.write(str(doc))
    mainhtml.find_links(doc, links_with_text)
    print(colored("Start to clone Loginpage!","blue"))
    clone.download_website(url, 1)
    screenshot.take_screenshot(url, 'screenshot.png',10)
    
    folder_path = cwd+ "\\" + "websites\\"+urlparse(url).netloc+"\\index.html"
    print(folder_path)
    screenshot.take_screenshot(folder_path, 'screenshot2.png', 4)

    #copy screenshots into another directory
    destination_directory = os.path.abspath('../frontend/src/screenshots')
    screenshot1_path = os.path.join(cwd, 'screenshot.png')
    destination_path = os.path.join(destination_directory, 'screenshot.png')
    shutil.copy(screenshot1_path, destination_path)

    
    screenshot2_path = os.path.join(cwd, 'screenshot2.png')
    destination_path = os.path.join(destination_directory, 'screenshot2.png')
    shutil.copy(screenshot2_path, destination_path)
    

    return jsonify({'message': 'Success'})

@app.route('/submit_data2', methods=['POST'])
def submit_data2():
    cwd = os.getcwd()
    data = request.get_json()  # Access the JSON data sent from the frontend
    url = data.get('inputValue')
    print(url)
    clone2.clonetry2(url)
    folder_path = cwd+ "\\" + "websites\\"+urlparse(url).netloc+"\\index.html"
    print(folder_path)
    screenshot.take_screenshot(folder_path, 'screenshot2.png', 4)

    #copy screenshots into another directory
    destination_directory = os.path.abspath('../frontend/src/screenshots')   
    screenshot2_path = os.path.join(cwd, 'screenshot2.png')
    destination_path = os.path.join(destination_directory, 'screenshot2.png')
    shutil.copy(screenshot2_path, destination_path)
    return jsonify({'message': 'Success'})

@app.route('/download_flask', methods=['POST'])
def download_flask():
    cwd = os.getcwd()
    data = request.get_json()  # Access the JSON data sent from the frontend
    url = data.get('inputValue')
    htmledit.insert_css_links(urlparse(url).netloc, 2)
    implement_backend.copy_files(urlparse(url).netloc, "index.html")
    implement_backend.implement_form()
    inputlist =[]
    inputnames = []
    implement_backend.get_vars_for_flask(inputlist, inputnames)
    print(inputlist)
    print(inputnames)
    with open('data.pkl', 'wb') as f:
        pickle.dump(inputnames, f)
    
    def convert_to_exe():
        command = f'pyinstaller -F --add-data "templates;templates" --add-data "static;static" --add-data "data.pkl;." flaskapp.py'
        subprocess.run(command, shell=True)

    
    convert_to_exe()
    return jsonify({'message': 'Success'})

@app.route('/ai_request', methods=['POST'])
def ai_request():
    # Get the domain from the frontend input
    data = request.get_json()
    domain = urlparse(data.get('input')).netloc

    # Call the request.py file and process the AI request
    subprocess.run(["python", "request.py"])

    # Move the generated HTML and CSS files to a separate directory
    destination_directory = os.path.abspath('../frontend/src/generated_files')
    shutil.move('index.html', os.path.join(destination_directory, 'index.html'))
    shutil.move('style.css', os.path.join(destination_directory, 'style.css'))

    return jsonify({'message': 'AI request successful'})

if __name__ == '__main__':
    app.run()