import os
import re
from collections import defaultdict

class ProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path
        self.file_data = defaultdict(list)
        self.analysis_results = {
            "languages": set(),
            "imports": set(),
            "technologies": set(),
            "data_structures": set()
        }
        self.language_extensions = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS'
        }

    def analyze_files(self):
        if os.path.isfile(self.project_path):
            self.analyze_file(self.project_path)
        else:
            for root, _, files in os.walk(self.project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)

    def analyze_file(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        lang = self.language_extensions.get(extension)
        if lang:
            self.file_data[lang].append(file_path)
            self.analysis_results["languages"].add(lang)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.detect_imports(content)
            self.detect_technologies(content)
            self.detect_data_structures(content)

    def detect_imports(self, content):
        includes = re.findall(r'#include\s*<([^>]+)>', content)
        imports = re.findall(r'(import\s+[a-zA-Z0-9_\.]+)', content)
        self.analysis_results["imports"].update(includes + imports)

    def detect_technologies(self, content):
        technologies = {
            'Flask': re.findall(r'\bFlask\b', content),
            'Django': re.findall(r'\bDjango\b', content),
            'React': re.findall(r'\bReact\b', content),
            'Node.js': re.findall(r'\bNode\.js\b', content),
            'Spring': re.findall(r'\bSpring\b', content),
        }
        for tech, matches in technologies.items():
            if matches:
                self.analysis_results["technologies"].add(tech)

    def detect_data_structures(self, content):
        data_structures = {
            'List': re.findall(r'\b(list|List)\b', content),
            'Array': re.findall(r'\b(array|Array)\b', content),
            'Dictionary': re.findall(r'\b(dict|Dict|dictionary|Dictionary)\b', content),
            'Tuple': re.findall(r'\b(tuple|Tuple)\b', content),
            'LinkedList': re.findall(r'\b(next|Next)\b', content),
            'Tree': re.findall(r'\b(left|Left|right|Right)\b', content),
            'HashTable': re.findall(r'\b(hash|Hash|hashtable|Hashtable)\b', content)
        }
        for ds, matches in data_structures.items():
            if matches:
                self.analysis_results["data_structures"].add(ds)

    def get_analysis_results(self):
        # Convert sets to lists for JSON serialization
        for key in self.analysis_results:
            self.analysis_results[key] = list(self.analysis_results[key])
        return self.analysis_results
