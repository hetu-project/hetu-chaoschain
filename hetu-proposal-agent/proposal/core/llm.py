from langchain_openai import ChatOpenAI
from typing import Optional
from proposal.config import settings

        # self.llm = ChatOpenAI(
        #     temperature=0.5,
        #     model_name=settings.OPENAI_MODEL,
        #     openai_api_key=settings.OPENAI_API_KEY
        # )

def get_chat_llm_instance(
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    streaming: bool = False,
    max_tokens: Optional[int] = None
) -> ChatOpenAI:
    """
    Create and return a configured ChatOpenAI instance
    
    Args:
        model_name: Model name, if not specified, use the default model from config
        temperature: Temperature parameter, controls output randomness, 0 means most deterministic, 1 means most creative
        streaming: Whether to use streaming output
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Configured ChatOpenAI instance
    """
    # Use provided parameters or default values from config
    model = model_name or settings.OPENAI_MODEL
    temp = temperature if temperature is not None else settings.default_temperature
    max_tokens = max_tokens or settings.max_tokens
    
    # Create ChatOpenAI instance
    llm = ChatOpenAI(
        model=model,
        temperature=temp,
        streaming=streaming,
        max_tokens=max_tokens,
        api_key=settings.OPENAI_API_KEY
    )
    
    return llm