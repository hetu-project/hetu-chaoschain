from langchain_core.messages import HumanMessage, AIMessage
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class ConversationMemory:
    def __init__(self):
        self.conversations = {}