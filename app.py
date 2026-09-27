import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_complaint():
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')

    if not title or not category or not description:
        return jsonify({'status': 'error', 'message': 'All fields are required!'})

    # main.exe (Absolute Path) निकालें
    exe_name = 'main.exe' if os.name == 'nt' else './main'
    exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), exe_name)
    try:
        # C++ exe को एग्जीक्यूट करें
        result = subprocess.run(
            [exe_path, title, category, description],
            capture_output=True,
            text=True
        )
        return jsonify({'status': 'success', 'message': 'Complaint submitted successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    complaints = []
    if os.path.exists('complaints.txt'):
        with open('complaints.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(' | ')
                if len(parts) == 3:
                    complaints.append({
                        'title': parts[0],
                        'category': parts[1],
                        'description': parts[2]
                    })
    return jsonify(complaints)

if __name__ == '__main__':
    app.run(debug=True)