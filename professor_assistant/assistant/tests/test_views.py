from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from assistant.models import Student, Score
from unittest.mock import patch

class ProcessInstructionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('process-instruction')
        self.student = Student.objects.create(
            student_id="1234",
            name="John Smith"
        )

    @patch('assistant.ai_helper.ProfessorAssistant.process_instruction')
    def test_add_student_instruction(self, mock_process):
        mock_process.return_value = {
            'action': 'ADD_STUDENT',
            'data': {
                'student_id': '5678',
                'name': 'Jane Doe'
            }
        }

        response = self.client.post(self.url, {
            'instruction': 'Add a new student named Jane Doe with ID 5678'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertTrue(Student.objects.filter(name='Jane Doe').exists())

    @patch('assistant.ai_helper.ProfessorAssistant.process_instruction')
    def test_add_score_instruction(self, mock_process):
        mock_process.return_value = {
            'action': 'ADD_SCORE',
            'data': {
                'student_id': '1234',
                'subject': 'Math',
                'score': 90.00
            }
        }

        response = self.client.post(self.url, {
            'instruction': 'Add a score of 90 for John Smith in Math'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Score.objects.count(), 1)
        self.assertEqual(Score.objects.first().score, 90.00)

    def test_invalid_instruction(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 