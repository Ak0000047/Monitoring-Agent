Monitoring Agent


**Components**

1. Agent ( agent.py / agent.exe )
   
A standalone Python script that retrieves system information every 5 seconds.

Sends the collected data to a backend API for storage in the database.

Can be run as a Python script or as a compiled executable.

Run as Python script:

**python agent.py --endpoint http://127.0.0.1:8000/processes/**

Run as executable:

After creating the executable using PyInstaller:

**pyinstaller --onefile agent.py**

Run the executable from its directory:

**agent.exe --endpoint http://127.0.0.1:8000/processes/**

2. Backend (Django project)

The backend is packaged in backend.rar .

Unzip backend.rar to a folder.

Run the Django server:

**python manage.py runserver**

Access the frontend at: http://127.0.0.1:8000/


3. Requirements
   
Python 3.10.8
Django
PyInstaller
Django Rest framework
psutill



4. Usage Workflow
   
Start the Django backend:

python manage.py runserver

Run the agent (Python script or executable) with the backend endpoint:

agent.exe --endpoint http://127.0.0.1:8000/processes/

The agent will collect system information every 5 seconds and send it to the backend.

View the data on the frontend at http://127.0.0.1:8000/ .

Make sure the backend is running before starting the agent.

.exe and .rar files are already included in the repository for convenience.
