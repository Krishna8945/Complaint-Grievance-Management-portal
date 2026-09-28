import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# System OS Check (Windows vs Linux)
exe_name = 'main.exe' if os.name == 'nt' else './main'
exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), exe_name)

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

    try:
        # C++ Binary Call with Default Status "Pending"
        result = subprocess.run(
            [exe_path, title, category, description, "Pending"],
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
                if len(parts) >= 3:
                    complaints.append({
                        'title': parts[0],
                        'category': parts[1],
                        'description': parts[2],
                        'status': parts[3] if len(parts) >= 4 else 'Pending'
                    })
    return jsonify(complaints)

# New Route: To Update Status (Admin Control)
@app.route('/update_status', methods=['POST'])
def update_status():
    index = int(request.form.get('index'))
    new_status = request.form.get('status') # 'Pending', 'In Progress', 'Resolved'

    if not os.path.exists('complaints.txt'):
        return jsonify({'status': 'error', 'message': 'No complaints found'})

    lines = []
    with open('complaints.txt', 'r') as file:
        lines = file.readlines()

    if 0 <= index < len(lines):
        parts = lines[index].strip().split(' | ')
        if len(parts) >= 3:
            # Update or attach new status
            lines[index] = f"{parts[0]} | {parts[1]} | {parts[2]} | {new_status}\n"
            
            with open('complaints.txt', 'w') as file:
                file.writelines(lines)
            return jsonify({'status': 'success', 'message': 'Status updated!'})

    return jsonify({'status': 'error', 'message': 'Invalid Index'})

if __name__ == '__main__':
    app.run(debug=True)