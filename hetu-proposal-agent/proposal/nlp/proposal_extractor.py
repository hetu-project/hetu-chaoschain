from typing import Dict, Any, Optional, List
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import json

class ProposalExtractor:
    """Extract proposal content from user text"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize proposal extractor
        
        Args:
            config: Configuration dictionary containing model settings, API keys, etc.
        """
        self.config = config or {}
        self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize LLM components and prompt templates"""
        model_name = self.config.get("model_name", "gpt-3.5-turbo")
        temperature = self.config.get("temperature", 0.0)
        api_key = self.config.get("api_key", os.getenv("OPENAI_API_KEY"))
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=api_key
        )
        
        self.extraction_prompt_template = PromptTemplate(
            input_variables=["input_text"],
            template="""
            Please analyze the following text to determine if it contains the intent to create a proposal and extract relevant content.
            
            User text:
            {input_text}
            
            Please perform two tasks:
            1. Determine if the user has the intention to create a new proposal
            2. If yes, please extract key elements of the proposal from the text
            
            Return the following content in JSON format:
            {{
              "has_proposal": true/false,  // Whether it contains proposal intent
              "title": "Proposal title",  // Extract or generate appropriate title
              "main_points": ["Point 1", "Point 2", ...],  // Main points of the proposal
              "background": "Background or motivation",  // Background description of the proposal
              "suggestions": ["Suggestion 1", "Suggestion 2", ...],  // Specific suggestions or action items
              "categories": ["Category 1", "Category 2", ...]  // Categories the proposal might belong to
            }}
            
            If the text does not contain proposal intent, just return {{"has_proposal": false}}.
            
            Return JSON format only, no other explanatory text.
            """
        )
        
        self.extraction_chain = LLMChain(llm=self.llm, prompt=self.extraction_prompt_template)
    
    def has_proposal_intent(self, text: str) -> bool:
        """
        Determine if the text contains intent to create a proposal
        
        Args:
            text: User input text
            
        Returns:
            Whether there is intent to create a proposal
        """
        try:
            result = self.extract_content(text)
            return result.get("has_proposal", False)
        except Exception:
            return False
    
    def extract_content(self, text: str) -> Dict[str, Any]:
        """
        Extract proposal-related content from text
        
        Args:
            text: User input text
            
        Returns:
            Extracted proposal content
        """
        try:
            response = self.extraction_chain.run(input_text=text)

            content = json.loads(response)
            return content
            
        except Exception as e:
            print(f"Proposal content extraction error: {str(e)}")
            return {
                "has_proposal": False,
                "title": None,
                "main_points": None,
                "background": None,
                "suggestions": None,
                "categories": None
            }
    
    def extract_and_format(self, text: str) -> Dict[str, Any]:
        """
        Extract and format proposal content, suitable for direct proposal creation
        
        Args:
            text: User input text
            
        Returns:
            Formatted proposal content, ready for proposal creation
        """
        content = self.extract_content(text)
        
        if not content.get("has_proposal", False):
            return None

        formatted_content = {
            "title": content.get("title", "Untitled Proposal"),
            "content": self._format_proposal_content(content),
            "tags": content.get("categories", []),
        }
        
        return formatted_content
    
    def _format_proposal_content(self, extracted_data: Dict[str, Any]) -> str:
        """
        Format extracted data into structured proposal content
        
        Args:
            extracted_data: Extracted proposal data
            
        Returns:
            Formatted proposal content text
        """
        content_parts = []
        
        if extracted_data.get("background"):
            content_parts.append(f"## Background\n\n{extracted_data['background']}\n")
        
        if extracted_data.get("main_points"):
            content_parts.append("## Main Points\n")
            for point in extracted_data["main_points"]:
                content_parts.append(f"- {point}")
            content_parts.append("\n")

        if extracted_data.get("suggestions"):
            content_parts.append("## Specific Suggestions\n")
            for suggestion in extracted_data["suggestions"]:
                content_parts.append(f"- {suggestion}")
            content_parts.append("\n")

        if not content_parts and "input_text" in self.config:
            content_parts.append(self.config["input_text"])
        
        return "\n".join(content_parts)