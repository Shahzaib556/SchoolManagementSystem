from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from students.models import Student
from attendance.models import StudentAttendance
from fees.models import FeePayment


def _attendance_summary(student):
    records = StudentAttendance.objects.filter(student=student).order_by("-date")
    total = records.count()
    present = records.filter(status="PRESENT").count()
    pct = round((present / total) * 100, 1) if total else 0
    return records[:60], pct


@login_required
def my_portal(request):
    """Landing page for STUDENT and PARENT roles — read-only, own-record-only access."""
    user = request.user
    if user.role == "STUDENT":
        student = getattr(user, "student_profile", None)
        if not student:
            return render(request, "portal/no_record.html")
        records, pct = _attendance_summary(student)
        fees = FeePayment.objects.filter(student=student).order_by("-due_date")
        return render(request, "portal/student_home.html", {
            "student": student, "attendance_records": records, "attendance_pct": pct, "fees": fees,
        })
    elif user.role == "PARENT":
        children = Student.objects.filter(parent=user)
        return render(request, "portal/parent_home.html", {"children": children})
    raise PermissionDenied


@login_required
def child_detail(request, pk):
    """A parent viewing one of their children's attendance/fee record — read-only."""
    if request.user.role != "PARENT":
        raise PermissionDenied
    student = get_object_or_404(Student, pk=pk, parent=request.user)
    records, pct = _attendance_summary(student)
    fees = FeePayment.objects.filter(student=student).order_by("-due_date")
    return render(request, "portal/student_home.html", {
        "student": student, "attendance_records": records, "attendance_pct": pct, "fees": fees, "is_parent_view": True,
    })
