# assistant/views.py
from typing import Dict, Any, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Max, Min
from .models import Student, Score
from .serializers import StudentSerializer, ScoreSerializer
from .ai_helper import ProfessorAssistant
import logging

logger = logging.getLogger(__name__)

class ProcessInstructionView(APIView):
    """
    API view for processing natural language instructions from professors.
    
    This view handles various types of instructions including:
    - Adding new students
    - Adding scores
    - Querying subjects
    - Summarizing scores
    """
    
    def post(self, request) -> Response:
        """
        Process a POST request containing a professor's instruction.
        
        Args:
            request: The HTTP request object containing the instruction
            
        Returns:
            Response object with the processing results or error message
        """
        instruction = request.data.get('instruction')
        if not instruction:
            logger.warning("Received request with no instruction")
            return Response(
                {'error': 'No instruction provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Processing instruction: {instruction}")
        assistant = ProfessorAssistant()
        processed_data = assistant.process_instruction(instruction)
        
        action_handlers = {
            'ADD_STUDENT': self._add_student,
            'ADD_SCORE': self._add_score,
            'GET_SUBJECT': self._get_subject,
            'SUMMARIZE_SCORES': self._summarize_scores
        }
        
        handler = action_handlers.get(processed_data['action'])
        if handler:
            return handler(processed_data['data'])
        
        logger.error(f"Invalid action received: {processed_data['action']}")
        return Response(
            {'error': 'Invalid action'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def _add_student(self, data: dict) -> Response:
        """
        Add a new student to the system.
        
        Args:
            data: Dictionary containing student information (student_id, name)
            
        Returns:
            Response object with success/error message and appropriate status code
        """
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Student added successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _add_score(self, data: dict) -> Response:
        """
        Add a score for a student in a subject.
        
        Args:
            data: Dictionary containing score information (student_id, subject, score)
            
        Returns:
            Response object with success/error message and appropriate status code
        """
        try:
            student = Student.objects.get(student_id=data['student_id'])
            score_data = {
                'student': student.id,
                'subject': data['subject'],
                'score': data['score']
            }
            serializer = ScoreSerializer(data=score_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'message': 'Score added successfully'},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _get_subject(self, data: dict) -> Response:
        """
        Get all subjects for a student.
        
        Args:
            data: Dictionary containing student information (student_id)
            
        Returns:
            Response object with list of subjects or error message
        """
        try:
            student = Student.objects.get(student_id=data['student_id'])
            scores = Score.objects.filter(student=student)
            subjects = [score.subject for score in scores]
            return Response({
                'student': student.name,
                'subjects': subjects
            })
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _summarize_scores(self, data: dict) -> Response:
        """
        Calculate summary statistics for scores in a subject.
        
        Args:
            data: Dictionary containing subject information (subject)
            
        Returns:
            Response object with summary statistics (average, highest, lowest, total_students)
            or error message if no scores found
        """
        subject = data.get('subject')
        scores = Score.objects.filter(subject=subject)
        if not scores:
            return Response(
                {'message': f'No scores found for {subject}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        summary = {
            'subject': subject,
            'average': sum(float(score.score) for score in scores) / len(scores),
            'highest': max(float(score.score) for score in scores),
            'lowest': min(float(score.score) for score in scores),
            'total_students': len(scores)
        }
        return Response(summary)