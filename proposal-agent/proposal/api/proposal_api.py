import os
import json
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from agents.agent import ProposalAgent
from proposal.database import ConversationMemory
from models.proposal import ProposalStatus

app = FastAPI()

# Initialize OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Initialize LLM model
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Initialize proposal agent and conversation memory
proposal_agent = ProposalAgent()
conversation_memory = ConversationMemory()

class UserMessage(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None

class AgentResponse(BaseModel):
    intent: str
    proposal_id: Optional[str] = None
    proposal_data: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None

@app.post("/api/process_message", response_model=AgentResponse)
async def process_message(user_input: UserMessage):
    """
    Process user messages, identify intent and execute corresponding operations
    """
    try:
        # Get conversation ID, create new if not exists
        conversation_id = user_input.conversation_id or conversation_memory.create_new_conversation(user_input.user_id)
        
        # Process user message
        # Process message and get structured response
        agent_result = proposal_agent.process_message(
            message=user_input.message,
            user_id=user_input.user_id,
            conversation_id=conversation_id
        )
        
        # Parse intent type
        intent = agent_result.get("type", "default")
        
        # Extract proposal data
        proposal_data = {
            "id": agent_result.get("proposal_id"),
            "title": agent_result.get("title"),
            "content": agent_result.get("formatted_content")
        } if intent == "proposal_created" else None
        
        # Build response
        agent_response = AgentResponse(
            intent=intent,
            conversation_id=conversation_id,
            proposal_id=proposal_data.get("id") if proposal_data else None,
            proposal_data=proposal_data
        )
        
        return agent_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
