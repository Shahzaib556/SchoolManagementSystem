"""
Seed script for Roshan Hunar Markaz School Management System.
Run with: python manage.py shell < seed.py
"""
import os
import django
import datetime
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User
from academics.models import AcademicYear, SchoolClass, Section, Subject
from teachers.models import Teacher
from students.models import Student
from fees.models import FeeStructure, FeePayment, Income, Expense
from attendance.models import StudentAttendance
from notices.models import Notice, Event
from sitepages.models import SiteSettings

print("Seeding database...")

# Superuser
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(username="admin", password="admin123", role=User.Role.SUPER_ADMIN, email="admin@rhm.edu.pk")
    print("Created superuser: admin / admin123")

# Academic year
year, _ = AcademicYear.objects.get_or_create(
    name="2025-2026",
    defaults={"start_date": datetime.date(2025, 8, 1), "end_date": datetime.date(2026, 6, 30), "is_current": True},
)

# Classes & sections
class_names = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]
sections = []
for cname in class_names:
    sc, _ = SchoolClass.objects.get_or_create(name=cname, academic_year=year)
    for sec_name in ["A", "B"]:
        sec, _ = Section.objects.get_or_create(school_class=sc, name=sec_name)
        sections.append(sec)

# Teachers
teacher_names = [("Ali", "Khan"), ("Sara", "Ahmed"), ("Bilal", "Hussain"), ("Ayesha", "Malik")]
teachers = []
for i, (fn, ln) in enumerate(teacher_names, start=1):
    username = f"teacher{i}"
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, password="changeme123", first_name=fn, last_name=ln, role=User.Role.TEACHER, email=f"{username}@rhm.edu.pk")
    else:
        u = User.objects.get(username=username)
    t, _ = Teacher.objects.get_or_create(user=u, defaults={
        "employee_id": f"EMP-{1000+i}", "qualification": "M.Ed", "experience_years": random.randint(2, 15),
        "salary": random.randint(40000, 90000), "date_joined": datetime.date(2022, 1, 1),
    })
    teachers.append(t)

for i, sec in enumerate(sections):
    sec.class_teacher = teachers[i % len(teachers)]
    sec.save()

# Subjects
subject_list = ["Mathematics", "English", "Science", "Urdu", "Islamiyat"]
for sc in SchoolClass.objects.all():
    for j, sub in enumerate(subject_list):
        Subject.objects.get_or_create(name=sub, code=f"{sc.name[-1]}-{sub[:3].upper()}", school_class=sc,
                                       defaults={"teacher": teachers[j % len(teachers)]})

# Students
first_names = ["Ahmed", "Zara", "Hamza", "Fatima", "Omar", "Mariam", "Usman", "Hira", "Bilawal", "Areeba"]
last_names = ["Raza", "Sheikh", "Chaudhry", "Baig", "Farooq"]
students = []
for i in range(1, 41):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    adm = f"RHM-{2025000+i}"
    sec = random.choice(sections)
    s, created = Student.objects.get_or_create(admission_number=adm, defaults={
        "roll_number": str(i), "first_name": fn, "last_name": ln,
        "date_of_birth": datetime.date(2015, random.randint(1, 12), random.randint(1, 28)),
        "gender": random.choice(["M", "F"]), "section": sec,
        "guardian_name": f"Mr. {ln}", "guardian_relation": "Father", "guardian_phone": "0300-1234567",
    })
    students.append(s)

# Fee structures & payments
for sc in SchoolClass.objects.all():
    fs, _ = FeeStructure.objects.get_or_create(school_class=sc, name="Monthly Tuition Fee", defaults={"amount": 3500, "frequency": "MONTHLY"})
    for st in Student.objects.filter(section__school_class=sc)[:8]:
        paid = random.choice([3500, 3500, 0, 1500])
        FeePayment.objects.get_or_create(
            student=st, fee_structure=fs, due_date=datetime.date.today(),
            defaults={
                "amount_due": 3500, "amount_paid": paid,
                "status": "PAID" if paid == 3500 else ("PARTIAL" if paid else "PENDING"),
                "paid_on": datetime.date.today() if paid else None,
                "receipt_number": f"RCPT-{st.admission_number}" if paid else None,
            },
        )

# Attendance for last 10 days
today = datetime.date.today()
for i in range(10):
    d = today - datetime.timedelta(days=i)
    for st in students:
        StudentAttendance.objects.get_or_create(student=st, date=d, defaults={"status": random.choice(["PRESENT", "PRESENT", "PRESENT", "ABSENT", "LATE"])})

# Notices & events
Notice.objects.get_or_create(title="Welcome to New Academic Year 2025-2026", defaults={"content": "We are excited to welcome all students and staff to the new academic year.", "audience": "ALL", "is_pinned": True})
Event.objects.get_or_create(title="Annual Sports Day", defaults={"date": today + datetime.timedelta(days=20), "location": "Main Ground", "description": "Join us for the annual sports day celebration."})

# Sample student login + linked parent login (for testing role-based portal access)
demo_student = students[0]
if not demo_student.user_id:
    su = User.objects.create_user(username="student1", password="changeme123", first_name=demo_student.first_name,
                                   last_name=demo_student.last_name, role=User.Role.STUDENT, email="student1@rhm.edu.pk")
    demo_student.user = su
if not User.objects.filter(username="parent1").exists():
    pu = User.objects.create_user(username="parent1", password="changeme123", first_name="Guardian", last_name="One",
                                   role=User.Role.PARENT, email="parent1@rhm.edu.pk")
else:
    pu = User.objects.get(username="parent1")
demo_student.parent = pu
demo_student.save()

# Sample accountant login
if not User.objects.filter(username="accountant1").exists():
    User.objects.create_user(username="accountant1", password="changeme123", first_name="Finance", last_name="Officer",
                              role=User.Role.ACCOUNTANT, email="accountant1@rhm.edu.pk")

# Sample income / funding records
income_samples = [
    ("Haji Abdul Rehman", "ZAKAT", 50000),
    ("Mrs. Nasreen Bibi", "SADQA", 5000),
    ("Anonymous Donor", "SADQA_E_FITAR", 15000),
    ("Malik Farms", "USHAR", 30000),
    ("Alumni Association", "DONATION", 25000),
]
for donor, itype, amount in income_samples:
    Income.objects.get_or_create(donor_name=donor, income_type=itype, amount=amount,
                                  defaults={"date": today - datetime.timedelta(days=random.randint(0, 25))})

# Default site settings (edit from /admin/ > Sitepages > Site Settings)
SiteSettings.objects.get_or_create(pk=1, defaults={
    "phone": "+92 300 1234567",
    "email": "info@roshanhunarmarkaz.edu.pk",
    "address": "Main Campus Road, Islamabad, Pakistan",
    "facebook_url": "https://facebook.com/roshanhunarmarkaz",
    "whatsapp_number": "+92 300 1234567",
    "bank_name": "Meezan Bank Ltd.",
    "account_title": "Roshan Hunar Markaz Trust",
    "account_number": "01234567890123",
    "iban": "PK00MEZN0001234567890123",
    "branch_code": "0123",
})

print("Seeding complete!")
print("Login as admin: admin / admin123")
print("Login as teacher: teacher1 / changeme123")
print(f"Login as student: student1 / changeme123  (record: {demo_student.admission_number})")
print("Login as parent: parent1 / changeme123  (linked to student1's child)")
print("Login as accountant: accountant1 / changeme123")
