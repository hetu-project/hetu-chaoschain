from typing import Dict, Any, Optional
import logging

# Import project components
from proposal.nlp.proposal_extractor import ProposalExtractor
from proposal.nlp.proposal_analyzer import ProposalAnalyzer
from proposal.nlp.proposal_formatter import ProposalFormatter
from proposal.services.proposal_service import ProposalService
from proposal.services.vote_service import VoteService
from proposal.core.llm import get_chat_llm_instance

logger = logging.getLogger(__name__)

class ProposalAgent:
    """Proposal AI Agent: Handle user requests and automated tasks related to proposals"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize proposal agent"""
        self.config = config or {}
        
        # Initialize components
        self.extractor = ProposalExtractor(config.get("extractor_config"))
        self.formatter = ProposalFormatter(config.get("formatter_config"))
        self.analyzer = ProposalAnalyzer(config.get("analyzer_config"))
        self.proposal_service = ProposalService()
        self.vote_service = VoteService()
        
        # Chat generation LLM
        self.chat_llm = get_chat_llm_instance(
            temperature=0.7,
            streaming=config.get("streaming", False)
        )
    
    
    def process_message(self, message: str, user_id: str) -> Dict[str, Any]:
        """Process user messages and execute corresponding proposal operations"""
        # Try to identify proposal creation intent
        if self.extractor.has_proposal_intent(message):
            return self._handle_proposal_creation(message, user_id)
            
        # Handle other intents...
        
        return {"type": "draft-proposal", "content": "I can help you create proposals, vote, or query proposal information."}
    
    def _handle_proposal_creation(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle proposal creation request"""
        # Step 1: Extract basic proposal content from message
        raw_proposal_data = self.extractor.extract_and_format(message)
        
        if not raw_proposal_data:
            return {
                "type": "error",
                "content": "Unable to extract valid proposal content from your message, please provide more details."
            }
        
        # Step 2: Format proposal content
        formatted_proposal = self.formatter.format_proposal(raw_proposal_data)
        
        # Step 3: Add creator information
        formatted_proposal["creator_id"] = user_id
        
        # Step 4: Analyze proposal quality (optional)
        analysis = self.analyzer.analyze_proposal(formatted_proposal)
        if analysis.get("overall_score", 7) < self.config.get("quality_threshold", 4):
            # Insufficient proposal quality, return feedback
            return {
                "type": "quality_feedback",
                "content": "Your proposal needs more details and argumentation. Please consider the following points:",
                "weaknesses": analysis.get("weaknesses", []),
                "proposal_draft": formatted_proposal
            }
        
        # Step 5: Create proposal
        proposal = self.proposal_service.create_proposal(**formatted_proposal)
        
        # Step 6: Return success response
        return {
            "type": "proposal_created",
            "proposal_id": proposal.get("proposal_id"),
            "title": proposal.get("title"),
            "content": "Your proposal has been successfully created! Other members can now vote and comment on it.",
            "formatted_content": formatted_proposal.get("content")
        }