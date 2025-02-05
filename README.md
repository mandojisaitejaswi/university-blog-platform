# University Blog Platform

## 📌 Project Overview
The **University Blog Platform** is an online space designed for university members to engage in discussions, share knowledge, and collaborate on various topics. Users can create and participate in customizable "Rooms," which facilitate academic discussions, extracurricular activities, and other shared interests.

## 🚀 Features
- **Rooms for academic and extracurricular discussions**
- **Role-based user management (Admins, Owners, and Members)**
- **Content sharing via text, images, videos, and links**
- **Post liking and commenting system**
- **Admin moderation for user and content management**
- **Polls for interactive discussions**

## 🏗 Database Structure
The platform uses a NoSQL database with the following collections:
- **Admin Collection**: Stores admin credentials and access levels.
- **Room Categories Collection**: Contains categories for organizing Rooms.
- **Rooms Collection**: Stores details of Rooms, their creators, and status.
- **Room Members Collection**: Manages user registration details.
- **Members Collection**: Stores registered users and their credentials.
- **Posts Collection**: Stores posts, including multimedia content, within Rooms.
- **Polls Collection**: Handles polling functionality with reference to posts and members.

## 🛠 Technology Stack
- **Backend**: Python (Flask/Django)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB (NoSQL)
- **Hosting & Deployment**: AWS/Heroku

## 🔧 Installation & Setup
Follow these steps to run the platform locally:
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
4. **Configure the database**:
   - Set up MongoDB and update connection details in `.env`.
5. **Start the application**:
   ```bash
   python main.py
   ```
6. **Access the platform**:
   - Open `http://localhost:5000` in your browser.

## 📖 Usage
- **Admins**: Manage platform operations, including Rooms and users.
- **Owners**: Create and moderate Rooms, approve members, and manage content.
- **Members**: Join Rooms, create posts, and interact with content.

## 🎨 UI Features
- **Admin Dashboard**: Manage users, Rooms, and posts.
- **Room Owner Panel**: Approve/reject members and moderate discussions.
- **Member Interface**: Post content, comment, and participate in polls.

## 👤 Authors
**Developed by:**
- Menaka Naga Sai Pothina
- Mandoji Sai Tejaswi
- Gali Udaya Rekha Chowdari
- Kadthala Udayasri

