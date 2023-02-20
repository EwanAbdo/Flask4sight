from flask import Flask, render_template, request, session
import subprocess

app = Flask(__name__)

# import pandas as pd
 
# # Read csv file in python_ flask
# df = pd.read_csv('linkedInFinal-programming-IdahoFallsIdahoUnitedStates.csv')

# import os
# from werkzeug.utils import secure_filename
 
# #*** Flask configuration
 
# # Define folder to save uploaded files to process further
# UPLOAD_FOLDER = os.path.join('static', 'uploads')
 
# # Define allowed files (for this example I want only csv file)
# ALLOWED_EXTENSIONS = {'csv'}
 
# # Configure upload file path flask
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# # Define secret key to enable session
# app.secret_key = 'This is your secret key to utilize session in Flask'  



@app.route('/')
def Web4Sight():
    return render_template('Web4Sight.html')

@app.route('/get_city',methods=['POST', 'GET'])
def get_city():
    output = request.form.to_dict()
    print(output)
    name = output["city"]
    return name

# @app.route('/get_path',methods=['POST', 'GET'])
# def get_path():
#     path = request.files['resume'].filename
#     print(path)
#     return path


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['resume']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return uploaded_file.filename

@app.route('/run_script', methods=['POST'])
def run_script():
    city = get_city()
    path = upload_file()
    subprocess.call(['python', 'LinkedIn6.py',path,city])
    # showData()
    return 'Script executed successfully!'

# @app.route('/show_data',  methods=("POST", "GET"))
# # def showData():
# #     # Convert pandas dataframe to html table flask
# #     df_html = df.to_html()
# #     return render_template('Web4Sight.html', data=df_html)
# def showData():
#     # Retrieving uploaded file path from session
#     data_file_path = session.get('uploaded_data_file_path', None)
 
    # # read csv file in python flask (reading uploaded csv file from uploaded server location)
    # uploaded_df = pd.read_csv(data_file_path)
 
    # # pandas dataframe to html table flask
    # uploaded_df_html = uploaded_df.to_html()
    # return render_template('show_csv_data.html', data_var = uploaded_df_html)


if __name__ == '__main__':
    app.run(debug=True)
