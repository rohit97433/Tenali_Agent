# Tenali v1: The Self-Healing Coding Agent

**Tenali** is a stateful, local-first coding assistant designed to bridge the gap between simple LLM chat interfaces and fully autonomous software engineering agents. Inspired by the legendary wit and strategic reasoning of Tenali Rama, this agent focuses on clever problem-solving, resourcefulness, and deep logical analysis.

Whether you are refactoring a 40-file React project or hunting down a logic bug in a Python script, Tenali acts as a "Co-Pilot" that can actually see your files, understand your architecture, and run your terminal.

---

## 🚀 Key Capabilities

*   **Autonomous Exploration:** Tenali doesn't guess. It uses tools to list directories and read files to understand your project’s structure before suggesting changes.
*   **Project Intelligence:** It automatically detects your tech stack (Node.js, Python, Rust, Go, etc.) and knows which commands to run for building and testing.
*   **The Self-Healing Loop:** If a fix causes a build error, Tenali reads the terminal output, analyzes the stack trace, and attempts a new fix. It doesn't stop until the code is verified.
*   **Local & Private:** Powered by **Ollama**, everything runs on your local hardware. Your proprietary code never leaves your machine.
*   **Stateful Memory:** Built on **LangGraph**, Tenali maintains a "shared blackboard" of memory across long development sessions.

---

## 🧠 The Architecture (ReAct Pattern)

Tenali operates on a **ReAct (Reason + Act)** pattern orchestrated through a Directed Cyclic Graph:

1.  **Analyze:** The LLM (The Brain) looks at your request and the current state of the project.
2.  **Act:** It selects a tool—like reading a file or running a shell command.
3.  **Observe:** It sees the output (e.g., "File saved" or "Build failed") and feeds it back into the reasoning loop.
4.  **Loop:** This cycle continues until the task is complete and verified.

---

## 🛠️ Setup Guide

### 1. Prerequisites
*   **Python 3.10+**
*   **Ollama** ([Download here](https://ollama.com/))
*   **Model:** Pull the default model (or any model of your choice):
    ```bash
    ollama pull qwen3:8b
    ```

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/Tenali.git
cd Tenali

# Setup virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🏁 How to Start

### Option 1: Manual Start
```bash
python main.py
```

### Option 2: The "tenali.bat" Shell Tool (Windows)
We've included a `tenali.bat` file that can be used as a global command.
1.  Add the folder path of this project to your **System Environment Variables** (under "Path").
2.  Open any terminal in any project and type `tenali` to wake the agent.

---

## 💡 Model Flexibility (Bring Your Own Brain)
Tenali is **model-agnostic**. You can swap the underlying LLM based on your hardware or the complexity of the task. 

*   **For Speed:** `qwen3:8b` or `llama3:8b`
*   **For Reasoning:** `qwen3:32b` or `llama3:70b`
*   **For Coding:** `deepseek-coder` or `codellama`

**To change models:** Simply update the `MODEL_NAME` variable in `main.py`.

---

## 📝 Example Tasks
*   *"List all files and tell me what this project does."*
*   *"Find the logic error in math_utils.py and fix it and update the changes in file ."*
*   *"Refactor my React components to use Tailwind CSS classes."*
*   *"Run the build command and fix any linting errors that appear."*

---

> **Built for developers, by a developer.** Tenali is your strategist in the terminal. Happy coding!

#AI #OpenSource #TenaliAgent #LangGraph #Ollama #Python #SoftwareEngineering

---

### One last thing...
When you upload this, make sure your **`requirements.txt`** has the manual list we discussed:
*   `langchain-ollama`
*   `langchain-core`
*   `langgraph`
*   `langchain-community`
