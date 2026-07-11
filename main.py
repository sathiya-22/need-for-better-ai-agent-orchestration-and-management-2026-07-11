import os
import google.generativeai as genai
from config import AppSettings
from typing import Dict, Any

# 1. Load settings from config.py and environment variables
settings = AppSettings()

# 2. Configure Google GenAI with the API key
genai.configure(api_key=settings.api_key)

# 3. Generic agent execution function
def execute_agent_task(agent_name: str, agent_prompt: str, user_input: str, model_config: Dict[str, Any]) -> str:
    """Executes a task using a generative AI model based on agent's role and input."""
    print(f"\n--- {agent_name.upper()} Agent ---")
    print(f"Input: {user_input[:150]}...") # Truncate for display

    model = genai.GenerativeModel(
        model_name=model_config['model_name'],
        generation_config={
            "temperature": model_config['temperature'],
            "max_output_tokens": model_config['max_tokens'],
        }
    )
    full_prompt = f"{agent_prompt}\n\nTask: {user_input}"
    try:
        response = model.generate_content(full_prompt)
        text_response = response.text
        print(f"Output: {text_response[:150]}...") # Truncate for display
        return text_response
    except Exception as e:
        print(f"Error executing agent {agent_name}: {e}")
        return f"Error: Failed to get response from {agent_name}."

# 4. Agent orchestrator
def orchestrate_agents(initial_query: str, settings: AppSettings) -> Dict[str, Any]:
    """Manages the flow of tasks between declaratively defined agents."""
    context: Dict[str, Any] = {"user_query": initial_query}
    model_config = {
        "model_name": settings.model_name,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    }

    print("\n--- Starting AI Agent Orchestration ---")
    print(f"Initial Query: {initial_query}")

    for step_idx, step in enumerate(settings.orchestration_flow):
        receiver = step["receiver"]
        input_key = step["input_key"]
        output_key = step["output_key"]
        task_description = step["task_description"]

        print(f"\n--- Step {step_idx + 1}: Executing {receiver} ({task_description}) ---")

        if receiver not in settings.agents:
            print(f"Error: Receiver agent '{receiver}' not defined in config. Skipping step.")
            continue

        agent_role_prompt = settings.agents[receiver]["role_prompt"]
        agent_input = context.get(input_key)

        if agent_input is None:
            if input_key == "user_query":
                agent_input = initial_query # Special handling for the initial user query
            else:
                print(f"Warning: Input key '{input_key}' not found in context for agent '{receiver}'. Skipping step.")
                continue

        response = execute_agent_task(
            agent_name=receiver,
            agent_prompt=agent_role_prompt,
            user_input=agent_input,
            model_config=model_config
        )
        context[output_key] = response
        print(f"Context updated: '{output_key}' stored.")

    print("\n--- Orchestration Complete ---")
    return context

# 5. Main execution block
if __name__ == "__main__":
    # Example usage: Define an initial problem for the agent system
    user_initial_query = "What are the latest advancements in quantum computing and their potential impact on cryptography?"
    
    # Run the orchestration process
    final_results = orchestrate_agents(user_initial_query, settings)

    print("\n--- Final Results Summary ---")
    for key, value in final_results.items():
        print(f"\n--- {key.upper()} ---\n{value[:700]}...\n") # Truncate for display
