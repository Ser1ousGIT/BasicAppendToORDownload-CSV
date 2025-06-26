from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import csv
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
REQUIRED_HEADERS = {'rollNo', 'name', 'age', 'city'}
EXISTING_FILE = os.path.join(os.path.dirname(__file__), 'data.csv')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csvfile' not in request.files:
        flash('No file part in request.')
        return redirect(request.url)

    file = request.files['csvfile']

    if file.filename == '':
        flash('No file selected. Please choose a CSV file.')
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash('Invalid file format. Please upload a CSV file.')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(temp_path)

    try:

        uploaded_rollnos = set()
        new_rows = []

        with open(temp_path, 'r', newline='', encoding='utf-8') as uploaded_file:
            reader = csv.DictReader(uploaded_file)
            if reader.fieldnames is None:
                flash('CSV file is empty or unreadable.')
                os.remove(temp_path)
                return redirect(url_for('index'))

            missing_headers = REQUIRED_HEADERS - set(reader.fieldnames)
            if missing_headers:
                flash(f'CSV file missing required columns: {", ".join(missing_headers)}')
                os.remove(temp_path)
                return redirect(url_for('index'))

            for row in reader:
                roll = row.get('rollNo')
                if roll and roll not in uploaded_rollnos:
                    uploaded_rollnos.add(roll)
                    new_rows.append(row)

        if not new_rows:
            flash('No valid records found in uploaded CSV (empty or duplicate rollNos).')
            os.remove(temp_path)
            return redirect(url_for('index'))

        existing_rollnos = set()
        if os.path.exists(EXISTING_FILE):
            with open(EXISTING_FILE, 'r', newline='', encoding='utf-8') as existing_file:
                reader = csv.DictReader(existing_file)
                for row in reader:
                    roll = row.get('rollNo')
                    if roll:
                        existing_rollnos.add(roll)


        filtered_rows = [row for row in new_rows if row['rollNo'] not in existing_rollnos]

        if filtered_rows:
            with open(EXISTING_FILE, 'a', newline='', encoding='utf-8') as existing_file:
                writer = csv.DictWriter(existing_file, fieldnames=filtered_rows[0].keys())
                for row in filtered_rows:
                    writer.writerow(row)
            flash(f'{len(filtered_rows)} new records appended successfully.')
        else:
            flash('All rollNos already exist in the system. No new data appended.')

    except Exception as e:
        flash(f'An error occurred while processing the CSV file: {str(e)}')
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return redirect(url_for('index'))

@app.route('/download')
def download_csv():
    if os.path.exists(EXISTING_FILE):
        return send_file(EXISTING_FILE, as_attachment=True, download_name='data.csv')
    else:
        flash('Data file not found.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)