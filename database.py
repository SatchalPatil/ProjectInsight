import sqlite3

def initialize_db():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''
        DROP TABLE IF EXISTS projects
    ''')
    c.execute('''
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            author_name TEXT NOT NULL,
            problem_statement TEXT NOT NULL,
            detected_languages TEXT,
            detected_imports TEXT,
            detected_technologies TEXT,
            detected_data_structures TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_project_info(project_info):
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (project_name, author_name, problem_statement, detected_languages, detected_imports, detected_technologies, detected_data_structures)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        project_info["project_name"], 
        project_info["author_name"], 
        project_info["problem_statement"], 
        ', '.join(project_info["detected_languages"]), 
        ', '.join(project_info["detected_imports"]), 
        ', '.join(project_info["detected_technologies"]), 
        ', '.join(project_info["detected_data_structures"])
    ))
    conn.commit()
    conn.close()
