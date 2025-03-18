from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import json

@dataclass
class Comment:
    """
    Comment data model
    
    Represents a comment on a proposal, including comment content, author and metadata
    """
    
    # Related information
    proposal_id: str
    commenter_id: str
    
    # Comment content
    content: str
    sentiment: str = "neutral"  # positive, negative, neutral, mixed
    
    # System fields
    comment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    # Additional information
    parent_id: Optional[str] = None  # Used for replying to other comments
    is_official: bool = False  # Mark if it's an official comment
    
    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_reply(self) -> bool:
        """Check if it's a reply comment"""
        return self.parent_id is not None
    
    def is_positive(self) -> bool:
        """Check if it's a positive comment"""
        return self.sentiment.lower() == "positive"
    
    def is_negative(self) -> bool:
        """Check if it's a negative comment"""
        return self.sentiment.lower() == "negative"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation
        
        Returns:
            Dictionary containing all comment data
        """
        return {
            "comment_id": self.comment_id,
            "proposal_id": self.proposal_id,
            "commenter_id": self.commenter_id,
            "content": self.content,
            "sentiment": self.sentiment,
            "created_at": self.created_at.isoformat(),
            "parent_id": self.parent_id,
            "is_official": self.is_official,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """
        Convert to JSON string
        
        Returns:
            Comment data in JSON format
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """
        Create comment instance from dictionary
        
        Args:
            data: Dictionary containing comment data
            
        Returns:
            Comment instance
        """
        # Handle datetime field
        created_at = datetime.fromisoformat(data["created_at"]) if isinstance(data["created_at"], str) else data["created_at"]
        
        return cls(
            comment_id=data["comment_id"],
            proposal_id=data["proposal_id"],
            commenter_id=data["commenter_id"],
            content=data["content"],
            sentiment=data.get("sentiment", "neutral"),
            created_at=created_at,
            parent_id=data.get("parent_id"),
            is_official=data.get("is_official", False),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Comment':
        """
        Create comment instance from JSON string
        
        Args:
            json_str: Comment data in JSON format
            
        Returns:
            Comment instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @staticmethod
    def validate_sentiment(sentiment: str) -> bool:
        """
        Validate if sentiment type is valid
        
        Args:
            sentiment: Sentiment type
            
        Returns:
            Whether valid or not
        """
        valid_sentiments = ["positive", "negative", "neutral", "mixed"]
        return sentiment.lower() in valid_sentiments