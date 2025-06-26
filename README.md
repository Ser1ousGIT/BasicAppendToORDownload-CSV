# CSV Append & Download Tool using Flask

A lightweight web app built with **Python Flask** that allows users to upload CSV files, append unique data to an existing CSV, and download the combined result.

---

# Features

- Upload CSV from browser
- Append only **unique records** (based on a chosen key like `rollNo`)
- Avoids duplicates both:
  - Within the uploaded file
  - Against the existing main CSV file
- Download the final merged CSV file
- Error handling with clear user feedback

---

# Requirements

- Python 3.x
- Flask
- Flask-CORS

Install dependencies:
```bash
pip install flask flask-cors
```

---

# Project Structure

```
project/
├── app.py                # Main Flask backend
├── data.csv              # Pre-existing CSV file to append to
├── import.csv            # File that has to be uploaded
├── templates/
│   └── index.html        
├── static/
│   └── style.css        
```

---

# How It Works

1. `data.csv` must already exist in the root folder.
2. Users upload a new `.csv` file with required fields like `rollNo`, `name`, `age`, etc.
3. The app:
   - Skips duplicate `rollNo`s in the uploaded file
   - Skips any row already in `data.csv` by comparing `rollNo`
4. Appends only new, valid entries.
5. User can download the updated `data.csv`.

---

# Default Config

- **Main CSV File:** `data.csv`
- **Unique Key:** `rollNo`
- **Required Headers:** `rollNo`, `name`, `age`, `city`  
  *(You can change this in `app.py` → `REQUIRED_HEADERS`)*

---

# Error Handling

The app gracefully handles:

- Uploading non-CSV files  
- Missing required headers  
- Uploading an empty CSV  
- Duplicates in the uploaded file  
- Duplicates against `data.csv`

User gets feedback through Flask `flash()` messages on the page.

---

# Running Locally

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

Developed by [Ser1ous/AnandSwaroop]
