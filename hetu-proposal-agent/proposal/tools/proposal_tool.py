from langchain.tools import BaseTool
from typing import Dict, List, Optional, Any
import json

from proposal.services.proposal_service import ProposalService
from proposal.nlp.proposal_analyzer import ProposalAnalyzer

class ProposalTool(BaseTool):
    name: str = "proposal_tool"
    description: str = "Manage community governance proposals and voting. Can be used to create proposals, view proposals, vote and analyze proposals."
    
    def __init__(self):
        """Initialize proposal tool and set required services"""
        super().__init__()
        self.proposal_service = ProposalService()
        self.proposal_analyzer = ProposalAnalyzer()
    
    def _run(self, action: str, **kwargs: Any) -> str:
        """
        Execute proposal tool operations
        
        Args:
            action: Operation to execute ('create', 'list', 'view', 'vote', 'analyze')
            **kwargs: Required parameters for operation
        
        Returns:
            Operation result as string
        """
        actions = {
            "create": self._create_proposal,
            "list": self._list_proposals,
            "view": self._view_proposal,
            "vote": self._vote_proposal,
            "analyze": self._analyze_proposal
        }
        
        if action in actions:
            return actions[action](**kwargs)
        else:
            return f"Unknown operation: {action}. Supported operations are: create, list, view, vote, analyze."
    
    def _create_proposal(self, title: str = "", description: str = "", **kwargs) -> str:
        """Create new proposal"""
        if not title or not description:
            return "Failed to create proposal: title and description cannot be empty"
        
        proposal = self.proposal_service.create_proposal(title, description)
        
        return f"""Created proposal #{proposal['proposal_id']}
        
                Title: {proposal['title']}

                Content: {proposal['description']}

                Users can vote using "support" or "oppose".
                        """
    
    def _list_proposals(self, status: str = None, **kwargs) -> str:
        """List all proposals or proposals with specified status"""
        proposals = self.proposal_service.list_proposals(status)
        
        if not proposals:
            return "No proposals currently"
        
        proposals_text = "\n\n".join([
            f"#{p['proposal_id']} - {p['title']} (Status: {p['status']}, Vote count: {p['vote_count']})"
            for p in proposals
        ])
        
        return f"Proposal list:\n\n{proposals_text}"
    
    def _view_proposal(self, proposal_id: str = "", **kwargs) -> str:
        """View specific proposal details"""
        if not proposal_id:
            return "Failed to view proposal: missing proposal ID"
        
        proposal = self.proposal_service.get_proposal(proposal_id)
        if not proposal:
            return f"Failed to view proposal: cannot find proposal with ID {proposal_id}"
        
        results = proposal.get('results', {})
        
        return f"""Proposal #{proposal_id}
        
                Title: {proposal['title']}

                Content: {proposal['description']}

                Voting status:
                - Support: {results.get('votes', {}).get('support', 0)} ({results.get('support_percentage', 0):.1f}%)
                - Oppose: {results.get('votes', {}).get('oppose', 0)} ({results.get('oppose_percentage', 0):.1f}%)

                Total votes: {results.get('total_votes', 0)}
                Status: {proposal['status']}
            """
    
    def _vote_proposal(self, proposal_id: str = "", voter_id: str = "default_user", 
                      vote: str = "", **kwargs) -> str:
        """Vote on proposal"""
        if not proposal_id or not vote:
            return "Vote failed: missing proposal ID or vote option"
        
        # Standardize voting options
        vote_map = {
            "support": "support", "yes": "support",
            "oppose": "oppose", "no": "oppose"
        }
        
        normalized_vote = vote_map.get(vote.lower())
        if not normalized_vote:
            return f"Vote failed: '{vote}' is not a valid voting option, please use 'support' or 'oppose'"
        
        success = self.proposal_service.add_vote(proposal_id, voter_id, normalized_vote)
        if not success:
            return "Vote failed: You may have already voted or the proposal is closed"
        
        return f"You have successfully voted on proposal #{proposal_id}: {normalized_vote}"
    
    def _analyze_proposal(self, proposal_id: str = "", **kwargs) -> str:
        """Analyze proposal and provide suggestions"""
        if not proposal_id:
            return "Failed to analyze proposal: missing proposal ID"
        
        proposal = self.proposal_service.get_proposal(proposal_id)
        if not proposal:
            return f"Failed to analyze proposal: cannot find proposal with ID {proposal_id}"
        
        # Use dedicated analyzer
        analysis_result = self.proposal_analyzer.analyze_proposal(proposal)
        vote_decision = self.proposal_analyzer.generate_vote_decision(analysis_result)
        
        return f"""Analysis for proposal #{proposal_id}:

                    Overall score: {analysis_result.get('overall_score', 5)}/10

                    Strengths:
                    - {'\n- '.join(analysis_result.get('strengths', ['No obvious strengths found']))}

                    Weaknesses:
                    - {'\n- '.join(analysis_result.get('weaknesses', ['No obvious weaknesses found']))}

                    Recommended vote: {vote_decision.get('vote_type', 'Undecided')}
                    Reason: {vote_decision.get('reason', 'No detailed reason')}
                """