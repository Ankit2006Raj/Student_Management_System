from django import forms
from .models import Student
from django.core.exceptions import ValidationError

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'phone', 'date_of_birth', 
                  'address', 'city', 'state', 'marks', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter full name',
                'required': True
            }),
            'roll_number': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter roll number',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter phone number (optional)'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter address (optional)',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter city (optional)'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter state (optional)'
            }),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter marks (0-100)',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'required': True
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0 or marks > 100:
                raise ValidationError('Marks must be between 0 and 100.')
        return marks
    
    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        instance = self.instance
        if Student.objects.filter(roll_number=roll_number).exclude(pk=instance.pk).exists():
            raise ValidationError('A student with this roll number already exists.')
        return roll_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        instance = self.instance
        if Student.objects.filter(email=email).exclude(pk=instance.pk).exists():
            raise ValidationError('A student with this email already exists.')
        return email


class StudentImportForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: name, roll_number, email, phone, marks',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
