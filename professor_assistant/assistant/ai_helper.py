from typing import Dict, Any, Optional
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import json
import logging
import os

logger = logging.getLogger(__name__)

class ProfessorAssistant:
    """
    A class that processes natural language instructions from professors using LangChain.
    
    This class handles the interpretation of text instructions and converts them into
    structured data for database operations.
    """
    
    def __init__(self) -> None:
        """Initialize the ProfessorAssistant with OpenAI language model."""
        logger.info("Initializing ProfessorAssistant")
        self.llm = OpenAI(temperature=0)
        
    def process_instruction(self, instruction: str) -> Dict[str, Any]:
        """
        Process a natural language instruction and extract relevant information.
        
        Args:
            instruction: A string containing the professor's instruction
            
        Returns:
            A dictionary containing the action type and extracted data
            
        Example:
            >>> assistant.process_instruction("Add a new student named John Smith with ID 1234")
            {'action': 'ADD_STUDENT', 'data': {'name': 'John Smith', 'student_id': '1234'}}
        """
        logger.info(f"Processing instruction: {instruction}")
        
        template = """
        Analyze the following professor instruction and extract the relevant information:
        Instruction: {instruction}
        
        Identify the action type (ADD_STUDENT, ADD_SCORE, GET_SUBJECT, SUMMARIZE_SCORES) and extract relevant details.
        
        Response format:
        {{"action": "ACTION_TYPE", "data": {{relevant_extracted_data}}}}
        """
        
        prompt = PromptTemplate(
            input_variables=["instruction"],
            template=template,
        )
        
        try:
            response = self.llm(prompt.format(instruction=instruction))
            logger.debug(f"LLM response: {response}")
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Error processing instruction: {str(e)}", exc_info=True)
            return {"action": "ERROR", "data": {"message": str(e)}}
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response into a structured format.
        
        Args:
            response: The raw response string from the language model
            
        Returns:
            A dictionary containing the parsed action and data
        """
        try:
            parsed_data = json.loads(response)
            logger.debug(f"Successfully parsed response: {parsed_data}")
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {str(e)}", exc_info=True)
            return {
                "action": "ERROR",
                "data": {"message": "Could not parse the response"}
            }
