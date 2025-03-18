from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import json

@dataclass
class Proposal:
    """
    Proposal Data Model
    
    Represents a complete proposal, including title, content, creator, status, votes and metadata
    """
    
    # Basic Information
    title: str
    content: str
    creator_id: str
    
    # System Fields
    proposal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Proposal Status
    status: str = "open"  # open, closed, approved, rejected
    
    # Categories and Tags
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    
    # Statistics
    vote_count: Dict[str, int] = field(default_factory=lambda: {"support": 0, "oppose": 0})
    comment_count: int = 0
    
    # Additional Data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update(self, **kwargs) -> None:
        """
        Update proposal attributes
        
        Args:
            **kwargs: Fields and values to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def add_vote(self, vote_type: str) -> None:
        """
        Add vote count
        
        Args:
            vote_type: Vote type ('support' or 'oppose')
        """
        if vote_type in self.vote_count:
            self.vote_count[vote_type] += 1
        else:
            self.vote_count[vote_type] = 1
    
    def increment_comment_count(self) -> None:
        """Increment comment count"""
        self.comment_count += 1
    
    def is_open(self) -> bool:
        """Check if the proposal is in open status"""
        return self.status == "open"
    
    def close(self, final_status: str = "closed") -> None:
        """
        Close the proposal
        
        Args:
            final_status: Final status ('closed', 'approved', 'rejected')
        """
        valid_statuses = ["closed", "approved", "rejected"]
        self.status = final_status if final_status in valid_statuses else "closed"
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation
        
        Returns:
            Dictionary containing all proposal data
        """
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "content": self.content,
            "creator_id": self.creator_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "status": self.status,
            "tags": self.tags,
            "categories": self.categories,
            "vote_count": self.vote_count,
            "comment_count": self.comment_count,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """
        Convert to JSON string
        
        Returns:
            Proposal data in JSON format
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Proposal':
        """
        Create proposal instance from dictionary
        
        Args:
            data: Dictionary containing proposal data
            
        Returns:
            Proposal instance
        """
        # Handle datetime fields
        created_at = datetime.fromisoformat(data["created_at"]) if isinstance(data["created_at"], str) else data["created_at"]
        updated_at = None
        if data.get("updated_at"):
            updated_at = datetime.fromisoformat(data["updated_at"]) if isinstance(data["updated_at"], str) else data["updated_at"]
        
        return cls(
            proposal_id=data["proposal_id"],
            title=data["title"],
            content=data["content"],
            creator_id=data["creator_id"],
            created_at=created_at,
            updated_at=updated_at,
            status=data["status"],
            tags=data.get("tags", []),
            categories=data.get("categories", []),
            vote_count=data.get("vote_count", {"support": 0, "oppose": 0}),
            comment_count=data.get("comment_count", 0),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Proposal':
        """
        Create proposal instance from JSON string
        
        Args:
            json_str: Proposal data in JSON format
            
        Returns:
            Proposal instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)