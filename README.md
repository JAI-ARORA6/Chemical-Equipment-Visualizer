📊 Chemical Equipment Parameter Visualizer

Hybrid Web + Desktop Application

A hybrid application that visualizes and analyzes chemical equipment data from CSV files.
The same Django backend powers both React (Web) and PyQt5 (Desktop) frontends.

You can try it here
https://chemical-equipment-visualizer4.netlify.app/
(Wait if site operation is slow)

## Desktop Application

Download the desktop application from GitHub Releases.

Run `app.exe` to start the PyQt5 desktop app.


🚀 Features

📂 Upload CSV file containing chemical equipment data
📈 Automatic data analysis using Pandas
📊 Interactive charts (Bar & Pie)
🗂️ Store and display last 5 uploaded datasets
📄 Generate downloadable PDF report with charts & summary
🔐 Basic Authentication
🌐 Web App (React)
🖥️ Desktop App (PyQt5)

🛠 Tech Stack

Layer	            Technology
Backend	            Django + Django REST Framework
Web Frontend	    React.js + Chart.js
Desktop Frontend	PyQt5 + Matplotlib
Data Processing	    Pandas
Database	        SQLite
Reports	            ReportLab + Matplotlib
Version Control	    Git & GitHub

📁 Project Structure

chemical-equipment-visualizer/
│
├── backend/
│   ├── core/
│   ├── equipment/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── utils.py
│   │   ├── urls.py
│   ├── db.sqlite3
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── Upload.js
│   └── package.json
│
├── desktop/
│   └── app.py
│
├── sample_equipment_data.csv
└── README.md

📄 Sample CSV Format

Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120,6.5,110
Valve B,Valve,100,5.8,115

⚙️ Backend Setup (Django)

1️⃣ Create & Activate Virtual Environment
cd backend
python -m venv venv


Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

2️⃣ Install Dependencies
pip install django djangorestframework pandas matplotlib reportlab

3️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

4️⃣ Create Superuser (for authentication)
python manage.py createsuperuser

5️⃣ Run Backend Server
python manage.py runserver
Backend runs at:
http://127.0.0.1:8000

🌐 Web Frontend Setup (React)

1️⃣ Install Dependencies
cd frontend
npm install

2️⃣ Start Web App
npm start


Web app runs at:

http://localhost:3000

🖥️ Desktop App Setup (PyQt5)

1️⃣ Install Dependencies
pip install pyqt5 requests matplotlib

2️⃣ Run Desktop App
cd desktop
python app.py

🔗 API Endpoints

Endpoint	             Method	      Description
/api/upload/	          POST	       Upload CSV
/api/history/	          GET	       Last 5 uploads
/api/download-report/	  GET	       Download PDF report

All endpoints use Basic Authentication.

📄 PDF Report Includes

Summary statistics
Equipment type distribution
Bar chart
Pie chart
Last 5 uploaded datasets
CSV upload
Charts
History
PDF download
Desktop + Web app


👤 Author
Jai Arora
