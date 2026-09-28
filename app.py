import os
import subprocess
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload Folder Setup
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# OS Execution Logic (Windows vs Linux)
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
    
    # Handle Image Upload
    image_file = request.files.get('image')
    image_name = ""
    if image_file and image_file.filename != '':
        image_name = secure_filename(image_file.filename)
        # Avoid file overwrite by timestamping if needed
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        image_file.save(image_path)

    if not title or not category or not description:
        return jsonify({'status': 'error', 'message': 'All fields are required!'})

    try:
        # Call C++ Binary via Subprocess
        result = subprocess.run(
            [exe_path, title, category, description, "Pending", image_name],
            capture_output=True,
            text=True
        )
        return jsonify({'status': 'success', 'message': 'Grievance submitted successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    complaints = []
    if os.path.exists('complaints.txt'):
        with open('complaints.txt', 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file):
                parts = line.strip().split(' | ')
                if len(parts) >= 3:
                    complaints.append({
                        'id': idx,
                        'title': parts[0],
                        'category': parts[1],
                        'description': parts[2],
                        'status': parts[3] if len(parts) >= 4 else 'Pending',
                        'image': parts[4] if len(parts) >= 5 else ''
                    })
    return jsonify(complaints)

@app.route('/update_status', methods=['POST'])
def update_status():
    index = request.form.get('index')
    new_status = request.form.get('status')
    
    if index is None or not new_status:
        return jsonify({'status': 'error', 'message': 'Invalid parameters'})
        
    index = int(index)
    if not os.path.exists('complaints.txt'):
        return jsonify({'status': 'error', 'message': 'No complaints record found'})

    lines = []
    with open('complaints.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if 0 <= index < len(lines):
        parts = lines[index].strip().split(' | ')
        if len(parts) >= 3:
            img = parts[4] if len(parts) >= 5 else ""
            lines[index] = f"{parts[0]} | {parts[1]} | {parts[2]} | {new_status} | {img}\n"
            
            with open('complaints.txt', 'w', encoding='utf-8') as file:
                file.writelines(lines)
            return jsonify({'status': 'success', 'message': 'Status updated successfully!'})

    return jsonify({'status': 'error', 'message': 'Complaint not found'})

if __name__ == '__main__':
    app.run(debug=True)