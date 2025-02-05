# University Blog Platform

## 📌 Project Overview
The **University Blog Platform** is a web-based application designed to facilitate content sharing and discussions within a university community. It allows students and faculty to post blogs, interact via comments, and engage with academic and social discussions in a structured manner.

## 🚀 Features
- User authentication and role-based access (Students & Faculty)
- Blog creation, editing, and deletion
- Commenting and discussion threads
- Like and share functionality
- Admin moderation controls
- Secure login and session management

## 🛠 Tech Stack
- **Backend**: Python (Flask/Django)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL/MySQL
- **Deployment**: AWS/Heroku

## 🔧 Installation & Setup
To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/university-blog-platform.git
   cd university-blog-platform
   ```
2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database**:
   - Configure `.env` with database credentials
   - Run migrations (if applicable):
     ```bash
     python manage.py migrate  # For Django
     flask db upgrade  # For Flask
     ```
5. **Start the application**:
   ```bash
   python main.py
   ```
6. **Access the platform**:
   - Open `http://localhost:5000` in your browser.

## 📖 Usage
- **Register/Login** as a student or faculty member.
- **Create blog posts** and share them with the university community.
- **Comment** on posts to engage in discussions.
- **Like and share** posts to promote academic knowledge sharing.
- **Admins** can moderate content and manage users.

## 🤝 Contributing
Contributions are welcome! To contribute:
- Fork the repository.
- Create a new feature branch.
- Submit a pull request with detailed explanations.
