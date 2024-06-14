from flask import Flask, request, render_template, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename
from analyzer import ProjectAnalyzer
import database

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = 'static'

database.initialize_db()

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        analyzer = ProjectAnalyzer(file_path)
        analyzer.analyze_files()
        project_info = {
            "project_name": request.form['project_name'],
            "author_name": request.form['author_name'],
            "problem_statement": request.form['problem_statement'],
            "detected_languages": analyzer.get_analysis_results()["languages"],
            "detected_imports": analyzer.get_analysis_results()["imports"],
            "detected_technologies": analyzer.get_analysis_results()["technologies"],
            "detected_data_structures": analyzer.get_analysis_results()["data_structures"]
        }
        database.store_project_info(project_info)
        
        return redirect(url_for('view_projects'))

@app.route('/projects')
def view_projects():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    projects = c.fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
