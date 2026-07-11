from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Any

class AppSettings(BaseSettings):
    """
    Application settings for AI agent orchestration, loaded from environment
    variables and declarative configurations.
    """
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_tokens: int = 1024
    # This field will automatically load from the GEMINI_API_KEY environment variable
    api_key: str

    # Declarative definitions of AI agents
    agents: Dict[str, Dict[str, str]] = {
        "researcher": {
            "role_prompt": "You are a diligent researcher. Your goal is to gather concise, factual information on a given topic. Respond directly with the information, no conversational filler or greetings.",
        },
        "summarizer": {
            "role_prompt": "You are a concise summarizer. Your goal is to take detailed information and distill it into a brief, easy-to-understand summary, focusing on key points and brevity. Do not add any conversational filler.",
        }
    }

    # Declarative definition of the orchestration flow
    # Each step defines an interaction:
    # - sender: The origin of the input (e.g., "user" or another agent's output key)
    # - receiver: The agent to execute the task
    # - input_key: The key in the shared context from which to retrieve input for the receiver
    # - output_key: The key in the shared context where the receiver's response will be stored
    # - task_description: A human-readable description of the step's purpose
    orchestration_flow: List[Dict[str, Any]] = [
        {
            "sender": "user",
            "receiver": "researcher",
            "input_key": "user_query",
            "output_key": "research_output",
            "task_description": "The researcher agent gathers information based on the user's initial query."
        },
        {
            "sender": "researcher",
            "receiver": "summarizer",
            "input_key": "research_output",
            "output_key": "summary_output",
            "task_description": "The summarizer agent condenses the researcher's findings into a brief summary."
        }
    ]
