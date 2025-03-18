from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import json


@dataclass
class Vote:
    """
    Vote Data Model
    
    Represents a vote on a proposal, including vote type, voter and metadata
    """
    
    # Related Information
    proposal_id: str
    voter_id: str
    
    # Vote Content
    vote_type: str  # "support", "oppose", "abstain"
    
    # Optional Vote Reason
    reason: Optional[str] = None
    
    # System Fields
    vote_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    # Additional Information
    weight: float = 1.0  # Vote weight, default is 1
    is_official: bool = False  # Mark if it's an official vote
    
    # Additional Data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_support(self) -> bool:
        """Check if it's a support vote"""
        return self.vote_type.lower() == "support"
    
    def is_oppose(self) -> bool:
        """Check if it's an oppose vote"""
        return self.vote_type.lower() == "oppose"
    
    def is_abstain(self) -> bool:
        """Check if it's an abstain vote"""
        return self.vote_type.lower() == "abstain"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation
        
        Returns:
            Dictionary containing all vote data
        """
        return {
            "vote_id": self.vote_id,
            "proposal_id": self.proposal_id,
            "voter_id": self.voter_id,
            "vote_type": self.vote_type,
            "reason": self.reason,
            "created_at": self.created_at.isoformat(),
            "weight": self.weight,
            "is_official": self.is_official,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """
        Convert to JSON string
        
        Returns:
            Vote data in JSON format
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Vote':
        """
        Create vote instance from dictionary
        
        Args:
            data: Dictionary containing vote data
            
        Returns:
            Vote instance
        """
        # Handle datetime field
        created_at = datetime.fromisoformat(data["created_at"]) if isinstance(data["created_at"], str) else data["created_at"]
        
        return cls(
            vote_id=data["vote_id"],
            proposal_id=data["proposal_id"],
            voter_id=data["voter_id"],
            vote_type=data["vote_type"],
            reason=data.get("reason"),
            created_at=created_at,
            weight=data.get("weight", 1.0),
            is_official=data.get("is_official", False),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Vote':
        """
        Create vote instance from JSON string
        
        Args:
            json_str: Vote data in JSON format
            
        Returns:
            Vote instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @staticmethod
    def validate_vote_type(vote_type: str) -> bool:
        """
        Validate if vote type is valid
        
        Args:
            vote_type: Vote type
            
        Returns:
            Whether valid
        """
        valid_vote_types = ["support", "oppose", "abstain"]
        return vote_type.lower() in valid_vote_types