import os
import google.generativeai as genai
from config import AppSettings
from typing import Dict, Any
import time
import logging

# 1. Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Load settings from config.py and environment variables
settings = AppSettings()

# 3. Configure Google GenAI with the API key
genai.configure(api_key=settings.api_key)

# 4. Generic agent execution function
def execute_agent_task(agent_name: str, agent_prompt: str, user_input: str, model_config: Dict[str, Any]) -> str:
    """Executes a task using a generative AI model based on agent's role and input."""
    logger.info(f"--- {agent_name.upper()} Agent ---")
    logger.info(f"Input for {agent_name}: {user_input[:150]}...") # Truncate for display

    model = genai.GenerativeModel(
        model_name=model_config['model_name'],
        generation_config={
            "temperature": model_config['temperature'],
            "max_output_tokens": model_config['max_tokens'],
        }
    )
    full_prompt = f"{agent_prompt}\n\nTask: {user_input}"
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            response = model.generate_content(full_prompt)
            text_response = response.text
            logger.info(f"Output from {agent_name}: {text_response[:150]}...") # Truncate for display
            return text_response
        except Exception as e:
            logger.warning(f"Error executing agent {agent_name}: {e}. Retrying in 1 second... (Attempt {retries + 1}/{max_retries})")
            time.sleep(1)
            retries += 1
    logger.error(f"Failed to get response from {agent_name} after {max_retries} retries.")
    return f"Error: Failed to get response from {agent_name}."

# 5. Agent orchestrator
def orchestrate_agents(initial_query: str, settings: AppSettings) -> Dict[str, Any]:
    """Manages the flow of tasks between declaratively defined agents."""
    if not initial_query:
        logger.error("Empty user query. Please provide a valid query.")
        return {}
    context: Dict[str, Any] = {"user_query": initial_query}
    model_config = {
        "model_name": settings.model_name,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    }

    logger.info("--- Starting AI Agent Orchestration ---")
    logger.info(f"Initial Query: {initial_query}")

    for step_idx, step in enumerate(settings.orchestration_flow):
        receiver = step["receiver"]
        input_key = step["input_key"]
        output_key = step["output_key"]
        task_description = step["task_description"]

        logger.info(f"--- Step {step_idx + 1}: Executing {receiver} ({task_description}) ---")

        if receiver not in settings.agents:
            logger.error(f"Receiver agent '{receiver}' not defined in config. Skipping step.")
            continue

        agent_role_prompt = settings.agents[receiver]["role_prompt"]
        agent_input = context.get(input_key)

        if agent_input is None:
            if input_key == "user_query":
                agent_input = initial_query # Special handling for the initial user query
            else:
                logger.warning(f"Input key '{input_key}' not found in context for agent '{receiver}'. Skipping step.")
                continue

        response = execute_agent_task(
            agent_name=receiver,
            agent_prompt=agent_role_prompt,
            user_input=agent_input,
            model_config=model_config
        )
        context[output_key] = response
        logger.info(f"Context updated: '{output_key}' stored.")

    logger.info("--- Orchestration Complete ---")
    return context

# 6. Main execution block
if __name__ == "__main__":
    # Example usage: Define an initial problem for the agent system
    user_initial_query = "What are the latest advancements in quantum computing and their potential impact on cryptography?"
    
    # Run the orchestration process
    final_results = orchestrate_agents(user_initial_query, settings)

    logger.info("\n--- Final Results Summary ---")
    for key, value in final_results.items():
        logger.info(f"\n--- {key.upper()} ---\n{value[:700]}...\n") # Truncate for display
