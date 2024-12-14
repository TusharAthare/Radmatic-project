from django.test import TestCase
from assistant.ai_helper import ProfessorAssistant
from unittest.mock import patch

class ProfessorAssistantTest(TestCase):
    def setUp(self):
        self.assistant = ProfessorAssistant()

    @patch('langchain_community.llms.OpenAI.__call__')
    def test_process_add_student_instruction(self, mock_llm):
        mock_llm.return_value = '''{"action": "ADD_STUDENT", "data": {"name": "John Smith", "student_id": "1234"}}'''
        
        result = self.assistant.process_instruction(
            "Add a new student named John Smith with ID 1234"
        )
        
        self.assertEqual(result['action'], 'ADD_STUDENT')
        self.assertEqual(result['data']['name'], 'John Smith')
        self.assertEqual(result['data']['student_id'], '1234')

    @patch('langchain_community.llms.OpenAI.__call__')
    def test_process_add_score_instruction(self, mock_llm):
        mock_llm.return_value = '''{"action": "ADD_SCORE", "data": {"student_id": "1234", "subject": "Math", "score": 90}}'''
        
        result = self.assistant.process_instruction(
            "Add a score of 90 for John Smith in Math"
        )
        
        self.assertEqual(result['action'], 'ADD_SCORE')
        self.assertEqual(result['data']['subject'], 'Math')
        self.assertEqual(result['data']['score'], 90)

    @patch('langchain_community.llms.OpenAI.__call__')
    def test_invalid_response_handling(self, mock_llm):
        mock_llm.return_value = 'Invalid JSON'
        
        result = self.assistant.process_instruction(
            "Invalid instruction"
        )
        
        self.assertEqual(result['action'], 'ERROR')
        self.assertTrue('message' in result['data']) 