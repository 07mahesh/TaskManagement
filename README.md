📦 Task Management System
---------------------------
A robust, user-centric Django application that helps teams assign, track, and communicate on tasks — featuring dynamic registration, department-based dashboards, profile image uploads, and real-time messaging between employees.

🚀 Features
-------------
- 🔐 User Registration with Roles
Dynamic form logic assigns roles (Admin, Employee) and displays personalized dashboards.
- 🖼️ Profile Management
Users can upload, edit, and display profile images, names, and email via dashboard.
- ✅ Task Tracking
Admins can assign tasks with status (Pending, In Progress, Completed) and priority levels.
- 🧑‍💼 Department Assignment
Tasks and users are linked to departments for better filtering and reporting.
- 💬 Live Messaging System
Employees can chat in real time using Django Channels, WebSocket-powered.
- 🌐 Role-Based Dashboards
Cleanly separated views and logic for admins vs employees.

🧱 Tech Stack
---------------
| Layer | Technology | 
| Backend | Django (with Django Channels) | 
| Frontend | HTML, CSS, JS (Jinja templating) | 
| Real-time | WebSockets via Django Channels | 
| Database | SQLite / PostgreSQL | 
| Media | Django ImageField, Media routing | 
| Auth | Django’s built-in auth system | 

📁 Setup Instructions
-----------------------
- Clone the Repository
git clone https://github.com/your-username/Taskmanagement.git
cd task-manager

- Create Virtual Environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

- Install Requirements
pip install -r requirements.txt

- Apply Migrations
python manage.py makemigrations
python manage.py migrate

- Create Superuser
python manage.py createsuperuser

- Run Development Server
python manage.py runserver


🔄 WebSocket Setup (Optional)
--------------------------------
If you're using Channels:
- Add ASGI_APPLICATION and CHANNEL_LAYERS in settings.py
- Run Redis (if needed):
docker run -p 6379:6379 -d redis


📂 Folder Structure Highlights
--------------------------------
task-manager/
├── employee/
│   ├── models.py      # UserProfile, Task, Department
│   ├── views.py       # Dashboards, Profile update, Messaging
│   ├── consumers.py   # Live chat WebSocket logic
│   └── templates/
│       └── chat.html  # Real-time messaging UI
├── static/            # CSS, JS, default images
├── media/             # Uploaded profile images
└── README.md









- 



- 
 







