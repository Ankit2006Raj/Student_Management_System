# 🎓 Advanced Student Management System

A **production-ready, enterprise-level** Django application for comprehensive student lifecycle management. Features include authentication, course management, attendance tracking, assignments, real-time notifications, REST API, and advanced analytics.

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)

## ✨ Key Features

### 🔐 Authentication & Authorization
- **User Registration & Login** - Secure authentication system
- **Role-Based Access Control** - Admin, Teacher, Student, Parent roles
- **User Profiles** - Extended profiles with avatars and preferences
- **Session Management** - Secure session handling
- **Password Management** - Secure password reset and change

### 👨‍🎓 Student Management
- **Complete CRUD Operations** - Create, Read, Update, Delete students
- **Advanced Search & Filtering** - Search by name, roll number, email, grade, class
- **Bulk Operations** - Import/Export CSV, Excel, bulk delete
- **Student Profiles** - Comprehensive profiles with photos, guardian info
- **Performance Tracking** - Marks, grades, attendance percentage
- **PDF Reports** - Generate detailed student reports

### 📚 Course Management
- **Course Creation** - Add courses with code, credits, semester
- **Teacher Assignment** - Assign teachers to courses
- **Student Enrollment** - Enroll students in courses
- **Course Analytics** - Track enrollment numbers and performance
- **Semester Tracking** - Manage academic years and semesters

### 📅 Attendance System
- **Daily Attendance** - Mark attendance (Present, Absent, Late, Excused)
- **Course-wise Tracking** - Track attendance per course
- **Attendance Reports** - Generate comprehensive attendance reports
- **Percentage Calculation** - Automatic attendance percentage
- **Bulk Marking** - Mark attendance for entire class at once
- **Historical Records** - View past attendance data

### 📝 Assignment Management
- **Create Assignments** - Add assignments with due dates, marks
- **File Attachments** - Attach assignment files
- **Student Submissions** - Students can submit assignments
- **Grading System** - Teachers can grade and provide feedback
- **Late Submission Tracking** - Automatic late submission detection
- **Submission History** - Track all submissions

### 📢 Communication
- **Announcements** - School-wide or class-specific announcements
- **Priority System** - Set announcement priorities
- **Expiration Dates** - Auto-expire old announcements
- **Notifications** - Real-time notification system
- **Email Notifications** - Optional email alerts
- **Notification Types** - Info, Success, Warning, Error, Assignment, Grade, Attendance

## 🚀 Quick Start

### Automated Setup (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the advanced setup script (creates everything!)
python setup_advanced.py

# 3. Start the server


### Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Run server
python manage.py runserver
```

### Access Points
- **Dashboard**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/
- **Login**: http://127.0.0.1:8000/accounts/login/
- 
## 🛠️ Technologies Used

### Backend
- **Django 4.2+** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL/SQLite** - Database
- **Celery** - Task queue (optional)
- **Redis** - Caching (optional)

### Frontend
- **HTML5, CSS3, JavaScript** - Core technologies
- **Chart.js** - Interactive charts
- **Font Awesome 6** - Icons
- **Google Fonts (Inter)** - Typography

### Libraries
- **openpyxl** - Excel file handling
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **django-filter** - Advanced filtering
- **django-cors-headers** - CORS support

## 📱 Screenshots
<img width="1348" height="597" alt="image" src="https://github.com/user-attachments/assets/e9e61d56-8ab5-4c9c-a4a6-c4debb0088e0" />
<img width="1280" height="649" alt="image" src="https://github.com/user-attachments/assets/8373c428-3cbc-4d6d-9de1-dea81c257357" />

### Dashboard
- Visual statistics cards
- Grade distribution chart
- Top performers list
- Quick action buttons

### Student List
- Advanced search and filters
- Sortable columns
- Bulk operations
- Pagination controls

### Student Profile
- Photo display
- Complete information
- Color-coded performance
- Quick edit/delete actions

### API Usage

```bash
# Get all students
curl -X GET http://localhost:8000/api/students/

# Create a student
curl -X POST http://localhost:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","roll_number":102,"email":"jane@example.com","marks":92.0}'

# Get student attendance
curl -X GET http://localhost:8000/api/students/1/attendance/

# Get dashboard statistics
curl -X GET http://localhost:8000/api/stats/
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Ankit Raj**

A passionate developer dedicated to creating efficient and scalable educational management solutions.

### Connect with Me

- 🐙 **GitHub**: [Ankit2006Rajand](https://github.com/Ankit2006Raj)
- 💼 **LinkedIn**: [Ankit Raj](https://www.linkedin.com/in/ankit-raj-226a36309)
- 📧 **Email**: [ankit9905163014@gmail.com](mailto:ankit9905163014@gmail.com)

## 📞 Support

For detailed setup instructions, see `SETUP_INSTRUCTIONS.md`

For any queries or support, feel free to reach out via email or connect on LinkedIn.

---

