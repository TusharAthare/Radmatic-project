from django.db import models
from typing import Any

class Student(models.Model):
    """
    Model representing a student in the system.
    
    Attributes:
        student_id: Unique identifier for the student
        name: Full name of the student
        created_at: Timestamp of when the student was added
    """
    
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.student_id})"

class Score(models.Model):
    """
    Model representing a student's score in a subject.
    
    Attributes:
        student: Reference to the Student model
        subject: Name of the subject
        score: Numerical score value
        created_at: Timestamp of when the score was recorded
    """
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    subject = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.student.name} - {self.subject}: {self.score}"
