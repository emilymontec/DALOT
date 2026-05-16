# ai/memory.py
from typing import List, Dict

class MemoryManager:
    """Simple in-memory chat history manager.
    In a real production app, this would use Redis or a database.
    """
    def __init__(self):
        self.sessions = {}
        
    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"role": role, "content": content})
        
        # Keep only the last 10 messages to avoid context overflow
        if len(self.sessions[session_id]) > 10:
            self.sessions[session_id] = self.sessions[session_id][-10:]
            
    def get_history(self, session_id: str) -> str:
        if session_id not in self.sessions:
            return "No history."
            
        history = ""
        for msg in self.sessions[session_id]:
            history += f"{msg['role'].capitalize()}: {msg['content']}\n"
        return history

# Global memory instance
memory = MemoryManager()
