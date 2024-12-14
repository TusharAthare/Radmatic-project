from django.test import TestCase
from assistant.models import Student, Score

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id="1234",
            name="John Smith"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "John Smith")
        self.assertEqual(self.student.student_id, "1234")

    def test_student_str_representation(self):
        self.assertEqual(str(self.student), "John Smith (1234)")

class ScoreModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id="1234",
            name="John Smith"
        )
        self.score = Score.objects.create(
            student=self.student,
            subject="Math",
            score=90.0
        )

    def test_score_creation(self):
        self.assertEqual(self.score.subject, "Math")
        self.assertEqual(float(self.score.score), 90.0)
        self.assertEqual(self.score.student, self.student)

    def test_score_str_representation(self):
        self.assertEqual(str(self.score), "John Smith - Math: 90.0") 