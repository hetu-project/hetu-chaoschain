from typing import Dict, Any, Optional, List
import os
import logging
from functools import lru_cache
import json

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


from proposal.core.llm import get_chat_llm_instance

from prompts.proposal_prompts import (
    ANALYSIS_TEMPLATE,
    VOTE_TEMPLATE,
    COMMENT_TEMPLATE
)

logger = logging.getLogger(__name__)

class ProposalAnalyzer:
    """Proposal Analyzer: Analyzes proposal content and provides voting and comment decision support"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize proposal analyzer"""
        self.config = config or {}
        self._initialize_llm()
        self._proposal_cache = {}
        
    def _initialize_llm(self) -> None:
        """Initialize LLM components and prompt templates"""
        analysis_config = self.config.get("analysis", {})
        vote_config = self.config.get("vote", {})
        comment_config = self.config.get("comment", {})
        
        self.analysis_llm = get_chat_llm_instance(
            model_name=analysis_config.get("model_name"),
            temperature=analysis_config.get("temperature", 0.0)
        )
        
        self.vote_llm = get_chat_llm_instance(
            model_name=vote_config.get("model_name"),
            temperature=vote_config.get("temperature", 0.0)
        )
        
        self.comment_llm = get_chat_llm_instance(
            model_name=comment_config.get("model_name"),
            temperature=comment_config.get("temperature", 0.7)
        )
        
        self.analysis_prompt_template = PromptTemplate(
            input_variables=["proposal_title", "proposal_content"],
            template=ANALYSIS_TEMPLATE
        )
        
        self.vote_prompt_template = PromptTemplate(
            input_variables=["analysis_result"],
            template=VOTE_TEMPLATE
        )
        
        self.comment_prompt_template = PromptTemplate(
            input_variables=["analysis_result", "sentiment"],
            template=COMMENT_TEMPLATE
        )
        
        self.analysis_chain = LLMChain(llm=self.analysis_llm, prompt=self.analysis_prompt_template)
        self.vote_chain = LLMChain(llm=self.vote_llm, prompt=self.vote_prompt_template)
        self.comment_chain = LLMChain(llm=self.comment_llm, prompt=self.comment_prompt_template)
    
    def analyze_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of the proposal
        
        Args:
            proposal: Proposal data dictionary, must include title and content
            
        Returns:
            Multi-dimensional analysis result dictionary
        """
        try:
            proposal_title = proposal.get("title", "")
            proposal_content = proposal.get("content", "")
            
            response = self.analysis_chain.run(
                proposal_title=proposal_title,
                proposal_content=proposal_content
            )
            
            analysis_result = json.loads(response)
            return analysis_result
            
        except Exception as e:
            print(f"Proposal analysis error: {str(e)}")
            return {
                "feasibility": 5,
                "relevance": 5,
                "cost_benefit": 5,
                "impact": 5,
                "risk": 5,
                "overall_score": 5.0,
                "strengths": ["Unable to complete analysis"],
                "weaknesses": ["Error occurred during analysis"]
            }
    
    def generate_vote_decision(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate voting decision based on analysis results
        
        Args:
            analysis_result: Proposal analysis results
            
        Returns:
            Decision dictionary containing vote type and reasoning
        """
        try:
            analysis_str = json.dumps(analysis_result, ensure_ascii=False)
            
            response = self.vote_chain.run(analysis_result=analysis_str)
            
            vote_decision = json.loads(response)
            return vote_decision
        
        except Exception as e:
            print(f"Vote decision error: {str(e)}")
            return {
                "vote_type": "oppose" if analysis_result.get("overall_score", 5) < 6 else "support",
                "reason": "Unable to generate detailed reason due to technical issues",
                "confidence": 0.5
            }
    
    def generate_comment(self, analysis_result: Dict[str, Any], 
                       sentiment: str = "neutral") -> Dict[str, Any]:
        """
        Generate comments based on analysis results
        
        Args:
            analysis_result: Proposal analysis results
            sentiment: Expected emotional tendency ("positive", "negative", "neutral")
            
        Returns:
            Dictionary containing comment content
        """
        try:
            analysis_str = json.dumps(analysis_result, ensure_ascii=False)
            
            response = self.comment_chain.run(
                analysis_result=analysis_str,
                sentiment=sentiment
            )
            
            comment_content = json.loads(response)
            return comment_content
        
        except Exception as e:
            print(f"Comment generation error: {str(e)}")
            return {
                "content": "This proposal has some strengths and areas for improvement.",
                "highlights": ["Complete proposal content"],
                "suggestions": ["Could provide more details"]
            }