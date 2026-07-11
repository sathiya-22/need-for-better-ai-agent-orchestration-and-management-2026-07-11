### AI Agent Orchestrator Prototype

**Problem:** The burgeoning field of AI agents faces a significant challenge in orchestration and management. Developers struggle to define, manage, and visualize the complex interactions within multi-agent systems. There's a clear need for declarative specifications, similar to infrastructure-as-code tools like Terraform, and robust visualization to understand agent behaviors and communication flows. Current approaches often involve imperative, hard-coded logic, which is difficult to scale and maintain, hindering the development of more complex and reliable AI systems.

**Approach:** This prototype demonstrates a simplified approach to declarative AI agent orchestration. It uses a `config.py` file to define agents with their roles and to specify an interaction flow as a sequence of steps. A central `main.py` orchestrator interprets this configuration, initializing agents (powered by Google's `gemini-2.5-flash` model) and executing their tasks in the defined order. This allows for clear separation of agent definition and operational logic, making systems more manageable, easier to extend, and more transparent.

**Usage:**
1.  **Set up your environment:** Ensure Python 3.9+ is installed.
2.  **Install dependencies:** `pip install -r requirements.txt`
3.  **Configure API Key:** Set your Google Gemini API key as an environment variable: `export GEMINI_API_KEY="YOUR_API_KEY"`.
4.  **Run the prototype:** `python main.py`

The system will simulate a research and summarization workflow, demonstrating how declarative specifications can manage agent interactions and provide a foundation for better agent system management.
