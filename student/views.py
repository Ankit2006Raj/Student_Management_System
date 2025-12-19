from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.http import HttpResponse, JsonResponse
from .models import Student, Course, Enrollment, Attendance, Assignment, Submission, Notification, Announcement
from .forms import StudentForm, StudentImportForm
import csv
import io
from openpyxl import Workbook
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_POST

def dashboard(request):
    """Dashboard with analytics"""
    total_students = Student.objects.filter(is_active=True).count()
    average_marks = Student.objects.filter(is_active=True).aggregate(Avg('marks'))['marks__avg'] or 0
    
    # Grade distribution
    grade_distribution = Student.objects.filter(is_active=True).values('grade').annotate(count=Count('grade')).order_by('grade')
    
    # Top performers
    top_performers = Student.objects.filter(is_active=True).order_by('-marks')[:5]
    
    # Recent students
    recent_students = Student.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'average_marks': round(average_marks, 2),
        'grade_distribution': list(grade_distribution),
        'top_performers': top_performers,
        'recent_students': recent_students,
    }
    return render(request, 'student/dashboard.html', context)

def student_list(request):
    """Student list with search, filter, sort, and pagination"""
    students = Student.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(roll_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filter by grade
    grade_filter = request.GET.get('grade', '')
    if grade_filter:
        students = students.filter(grade=grade_filter)
    
    # Filter by marks range
    marks_min = request.GET.get('marks_min', '')
    marks_max = request.GET.get('marks_max', '')
    if marks_min:
        students = students.filter(marks__gte=marks_min)
    if marks_max:
        students = students.filter(marks__lte=marks_max)
    
    # Sort functionality
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['name', '-name', 'roll_number', '-roll_number', 'marks', '-marks', 'created_at', '-created_at']
    if sort_by in valid_sorts:
        students = students.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'grade_filter': grade_filter,
        'marks_min': marks_min,
        'marks_max': marks_max,
        'sort_by': sort_by,
    }
    return render(request, 'student/student_list.html', context)

def student_detail(request, pk):
    """Detailed view of a student"""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student/detail.html', {'student': student})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student/student_form.html', {'form': form, 'title': 'Add Student'})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student/student_form.html', {'form': form, 'title': 'Edit Student'})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'student/student_confirm_delete.html', {'student': student})

@require_POST
def bulk_delete(request):
    """Bulk delete students"""
    student_ids = request.POST.getlist('student_ids[]')
    if student_ids:
        Student.objects.filter(id__in=student_ids).delete()
        return JsonResponse({'success': True, 'message': f'{len(student_ids)} students deleted successfully!'})
    return JsonResponse({'success': False, 'message': 'No students selected'})

def export_csv(request):
    """Export students to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Roll Number', 'Email', 'Phone', 'Marks', 'Grade', 'City', 'State'])
    
    students = Student.objects.filter(is_active=True).values_list(
        'name', 'roll_number', 'email', 'phone', 'marks', 'grade', 'city', 'state'
    )
    for student in students:
        writer.writerow(student)
    
    return response

def export_excel(request):
    """Export students to Excel"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Students"
    
    # Headers
    headers = ['Name', 'Roll Number', 'Email', 'Phone', 'Marks', 'Grade', 'City', 'State', 'Created At']
    ws.append(headers)
    
    # Data
    students = Student.objects.filter(is_active=True)
    for student in students:
        ws.append([
            student.name,
            student.roll_number,
            student.email,
            student.phone or '',
            student.marks,
            student.grade,
            student.city or '',
            student.state or '',
            student.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
    wb.save(response)
    
    return response

def import_csv(request):
    """Import students from CSV"""
    if request.method == 'POST':
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('import_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                
                for row in reader:
                    try:
                        Student.objects.create(
                            name=row.get('name', ''),
                            roll_number=int(row.get('roll_number', 0)),
                            email=row.get('email', ''),
                            phone=row.get('phone', ''),
                            marks=float(row.get('marks', 0)),
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        continue
                
                messages.success(request, f'Successfully imported {success_count} students. {error_count} errors.')
                return redirect('student_list')
                
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
                return redirect('import_csv')
    else:
        form = StudentImportForm()
    
    return render(request, 'student/import.html', {'form': form})


# ==================== COURSE VIEWS ====================

def course_list(request):
    """List all courses"""
    courses = Course.objects.filter(is_active=True)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        courses = courses.filter(
            Q(code__icontains=search) | Q(name__icontains=search)
        )
    
    context = {'courses': courses, 'search': search}
    return render(request, 'student/course_list.html', context)


def course_detail(request, pk):
    """Course detail with enrolled students"""
    course = get_object_or_404(Course, pk=pk)
    enrollments = Enrollment.objects.filter(course=course, is_active=True)
    assignments = Assignment.objects.filter(course=course, is_active=True)
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'assignments': assignments,
    }
    return render(request, 'student/course_detail.html', context)


def course_create(request):
    """Create new course"""
    if request.method == 'POST':
        # Handle form submission
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description')
        credits = request.POST.get('credits', 3)
        semester = request.POST.get('semester')
        
        Course.objects.create(
            code=code,
            name=name,
            description=description,
            credits=credits,
            semester=semester,
            teacher=request.user
        )
        messages.success(request, 'Course created successfully!')
        return redirect('course_list')
    
    return render(request, 'student/course_form.html', {'title': 'Add Course'})


def course_update(request, pk):
    """Update course"""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.code = request.POST.get('code')
        course.name = request.POST.get('name')
        course.description = request.POST.get('description')
        course.credits = request.POST.get('credits', 3)
        course.semester = request.POST.get('semester')
        course.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('course_detail', pk=pk)
    
    return render(request, 'student/course_form.html', {'course': course, 'title': 'Edit Course'})


def course_delete(request, pk):
    """Delete course"""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.is_active = False
        course.save()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    
    return render(request, 'student/course_confirm_delete.html', {'course': course})


# ==================== ATTENDANCE VIEWS ====================

def attendance_list(request):
    """View attendance records"""
    attendances = Attendance.objects.all().order_by('-date')
    
    # Filters
    student_id = request.GET.get('student')
    course_id = request.GET.get('course')
    date = request.GET.get('date')
    status = request.GET.get('status')
    
    if student_id:
        attendances = attendances.filter(student_id=student_id)
    if course_id:
        attendances = attendances.filter(course_id=course_id)
    if date:
        attendances = attendances.filter(date=date)
    if status:
        attendances = attendances.filter(status=status)
    
    # Pagination
    paginator = Paginator(attendances, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    students = Student.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'students': students,
        'courses': courses,
    }
    return render(request, 'student/attendance_list.html', context)


def mark_attendance(request):
    """Mark attendance for students"""
    if request.method == 'POST':
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        
        course = get_object_or_404(Course, pk=course_id)
        enrollments = Enrollment.objects.filter(course=course, is_active=True)
        
        for enrollment in enrollments:
            status = request.POST.get(f'status_{enrollment.student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=enrollment.student,
                    course=course,
                    date=date,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance_list')
    
    courses = Course.objects.filter(is_active=True)
    return render(request, 'student/mark_attendance.html', {'courses': courses})


def attendance_report(request):
    """Generate attendance report"""
    students = Student.objects.filter(is_active=True)
    
    report_data = []
    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='P').count()
        percentage = (present / total * 100) if total > 0 else 0
        
        report_data.append({
            'student': student,
            'total': total,
            'present': present,
            'percentage': round(percentage, 2)
        })
    
    context = {'report_data': report_data}
    return render(request, 'student/attendance_report.html', context)


# ==================== ASSIGNMENT VIEWS ====================

def assignment_list(request):
    """List all assignments"""
    assignments = Assignment.objects.filter(is_active=True).order_by('-due_date')
    
    # Filter by course
    course_id = request.GET.get('course')
    if course_id:
        assignments = assignments.filter(course_id=course_id)
    
    courses = Course.objects.filter(is_active=True)
    
    context = {
        'assignments': assignments,
        'courses': courses,
    }
    return render(request, 'student/assignment_list.html', context)


def assignment_detail(request, pk):
    """Assignment detail with submissions"""
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = Submission.objects.filter(assignment=assignment)
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'student/assignment_detail.html', context)


def assignment_create(request):
    """Create new assignment"""
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        total_marks = request.POST.get('total_marks', 100)
        
        course = get_object_or_404(Course, pk=course_id)
        
        assignment = Assignment.objects.create(
            course=course,
            title=title,
            description=description,
            due_date=due_date,
            total_marks=total_marks,
            created_by=request.user
        )
        
        if request.FILES.get('attachment'):
            assignment.attachment = request.FILES['attachment']
            assignment.save()
        
        messages.success(request, 'Assignment created successfully!')
        return redirect('assignment_list')
    
    courses = Course.objects.filter(is_active=True)
    return render(request, 'student/assignment_form.html', {'courses': courses, 'title': 'Create Assignment'})


def assignment_update(request, pk):
    """Update assignment"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.method == 'POST':
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.due_date = request.POST.get('due_date')
        assignment.total_marks = request.POST.get('total_marks', 100)
        
        if request.FILES.get('attachment'):
            assignment.attachment = request.FILES['attachment']
        
        assignment.save()
        messages.success(request, 'Assignment updated successfully!')
        return redirect('assignment_detail', pk=pk)
    
    courses = Course.objects.filter(is_active=True)
    return render(request, 'student/assignment_form.html', {
        'assignment': assignment,
        'courses': courses,
        'title': 'Edit Assignment'
    })


def assignment_delete(request, pk):
    """Delete assignment"""
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.is_active = False
        assignment.save()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('assignment_list')
    
    return render(request, 'student/assignment_confirm_delete.html', {'assignment': assignment})


def submit_assignment(request, pk):
    """Submit assignment"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, pk=student_id)
        submission_text = request.POST.get('submission_text')
        
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            submission_text=submission_text
        )
        
        if request.FILES.get('submission_file'):
            submission.submission_file = request.FILES['submission_file']
            submission.save()
        
        messages.success(request, 'Assignment submitted successfully!')
        return redirect('assignment_detail', pk=pk)
    
    students = Student.objects.filter(is_active=True)
    return render(request, 'student/submit_assignment.html', {
        'assignment': assignment,
        'students': students
    })


# ==================== ANNOUNCEMENT VIEWS ====================

def announcement_list(request):
    """List all announcements"""
    announcements = Announcement.objects.filter(is_active=True).order_by('-priority', '-created_at')
    
    context = {'announcements': announcements}
    return render(request, 'student/announcement_list.html', context)


def announcement_create(request):
    """Create new announcement"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        target_class = request.POST.get('target_class')
        priority = request.POST.get('priority', 0)
        
        Announcement.objects.create(
            title=title,
            content=content,
            target_class=target_class,
            priority=priority,
            created_by=request.user
        )
        
        messages.success(request, 'Announcement created successfully!')
        return redirect('announcement_list')
    
    return render(request, 'student/announcement_form.html')


# ==================== NOTIFICATION VIEWS ====================

def notification_list(request):
    """List user notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    context = {'notifications': notifications}
    return render(request, 'student/notification_list.html', context)


def mark_notification_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('notification_list')


# ==================== PDF REPORT GENERATION ====================

def student_report_pdf(request, pk):
    """Generate PDF report for student"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from io import BytesIO
    
    student = get_object_or_404(Student, pk=pk)
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=30,
        alignment=1  # Center
    )
    elements.append(Paragraph('Student Report', title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Student Info
    data = [
        ['Name:', student.name],
        ['Roll Number:', str(student.roll_number)],
        ['Email:', student.email],
        ['Phone:', student.phone or 'N/A'],
        ['Class:', student.class_name or 'N/A'],
        ['Marks:', f'{student.marks}%'],
        ['Grade:', student.grade],
        ['Attendance:', f'{student.get_attendance_percentage()}%'],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="student_report_{student.roll_number}.pdf"'
    
    return response
