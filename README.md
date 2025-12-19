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

### 📊 Analytics & Reports
- **Dashboard** - Visual statistics and charts
- **Grade Distribution** - Interactive charts showing grade breakdown
- **Top Performers** - Highlight best students
- **Attendance Analytics** - Overall attendance statistics
- **Performance Trends** - Track student performance over time
- **Export Reports** - CSV, Excel, PDF formats

### 🔌 REST API
- **Complete API** - RESTful API for all resources
- **Authentication** - Token-based authentication
- **Filtering & Search** - Advanced query capabilities
- **Pagination** - Efficient data handling
- **Documentation** - Complete API documentation

### 🎨 Modern UI/UX
- **Responsive Design** - Works on all devices
- **Glassmorphism Effects** - Modern, beautiful design
- **Smooth Animations** - Professional transitions
- **Dark Mode Support** - User preference-based theming
- **Interactive Charts** - Chart.js integration
- **Font Awesome Icons** - Professional iconography
- **Color-Coded Grades** - Visual performance indicators
- **Navigation Bar** - Sticky, responsive navigation

## 🚀 Quick Start

### Automated Setup (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the advanced setup script (creates everything!)
python setup_advanced.py

# 3. Start the server
python manage.py runserver

# 4. Open browser to http://127.0.0.1:8000/
```

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

### Default Login Credentials (After setup_advanced.py)
- **Admin**: username: `admin`, password: `admin123`
- **Teacher**: username: `teacher1`, password: `teacher123`
- **Student**: username: `student1`, password: `student123`

### Access Points
- **Dashboard**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/
- **Login**: http://127.0.0.1:8000/accounts/login/

## 📁 Project Structure

```
Student_Record_Management_System/
├── student/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html                    # Base template with modern UI
│   │   └── student/
│   │       ├── dashboard.html           # Analytics dashboard
│   │       ├── student_list.html        # List with search/filter
│   │       ├── student_form.html        # Add/Edit form
│   │       ├── detail.html              # Student profile
│   │       ├── student_confirm_delete.html
│   │       └── import.html              # CSV import
│   ├── models.py                        # Enhanced Student model
│   ├── views.py                         # All CRUD + features
│   ├── forms.py                         # Forms with validation
│   ├── urls.py                          # URL patterns
│   └── admin.py
├── student_management/
│   ├── settings.py                      # Project settings
│   └── urls.py                          # Main URL config
├── media/                               # Uploaded files
├── requirements.txt                     # Dependencies
├── sample_students.csv                  # Sample import file
├── SETUP_INSTRUCTIONS.md               # Detailed setup guide
└── manage.py
```

## 📊 Student Model

```python
class Student(models.Model):
    # Basic Information
    name = models.CharField(max_length=100)
    roll_number = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    
    # Academic
    marks = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
```

## 📥 CSV Import Format

```csv
name,roll_number,email,phone,marks
John Doe,101,john@email.com,1234567890,85.5
Jane Smith,102,jane@email.com,0987654321,92.0
```

See `sample_students.csv` for a complete example.

## 🎓 Grade System

| Grade | Marks Range | Description |
|-------|-------------|-------------|
| A     | 90-100      | Excellent   |
| B     | 80-89       | Very Good   |
| C     | 70-79       | Good        |
| D     | 60-69       | Average     |
| F     | 0-59        | Fail        |

Grades are automatically calculated when saving student records.

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

## 🔮 Future Enhancements

### Phase 1 (Next 3 months)
- [ ] Real-time chat system
- [ ] Video conferencing integration
- [ ] Advanced analytics with ML
- [ ] Mobile app (React Native)

### Phase 2 (Next 6 months)
- [ ] Fee management
- [ ] Library management
- [ ] Transport management
- [ ] Exam management

### Phase 3 (Next 12 months)
- [ ] Hostel management
- [ ] Timetable generation
- [ ] Automated report cards
- [ ] Biometric attendance
- [ ] ID card generation
- [ ] SMS notifications

## 📚 Documentation

Comprehensive documentation is available:

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project documentation
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - REST API reference
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment guide
- **[FEATURES_SUMMARY.md](FEATURES_SUMMARY.md)** - What's new in v2.0

## 📝 Usage Examples

### Django ORM Operations

```python
from student.models import Student, Course, Enrollment, Attendance

# Create a student
student = Student.objects.create(
    name="John Doe",
    roll_number=101,
    email="john@example.com",
    marks=85.5,
    class_name="12A"
)

# Enroll student in a course
course = Course.objects.get(code="MATH101")
Enrollment.objects.create(student=student, course=course)

# Mark attendance
Attendance.objects.create(
    student=student,
    course=course,
    date=timezone.now().date(),
    status='P'
)

# Get student's attendance percentage
percentage = student.get_attendance_percentage()

# Search students
results = Student.objects.filter(name__icontains="John")

# Get top performers
top_students = Student.objects.filter(marks__gte=90).order_by('-marks')

# Calculate average
from django.db.models import Avg
avg_marks = Student.objects.aggregate(Avg('marks'))

# Grade distribution
from django.db.models import Count
distribution = Student.objects.values('grade').annotate(count=Count('grade'))
```

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

Created with ❤️ for educational and professional use.

## 📞 Support

For detailed setup instructions, see `SETUP_INSTRUCTIONS.md`

---

**Status**: ✅ Production-Ready Industry-Level Application

**Last Updated**: December 2024
"# Student_Management_System" 
