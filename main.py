"""
MAIN.PY - Agentic Coding Assistant (LangGraph StateGraph)
===========================================================
A coding agent that can:
 1. Analyze your command (understand what you want)
 2. Read your project files
 3. Find errors in code
 4. Write fixes
 5. Run build/test based on project type

Uses StateGraph instead of deprecated create_react_agent.

BEFORE RUNNING:
 1. Install Ollama → https://ollama.com/download
 2. Pull a model → ollama pull qwen3:8b
 3. Install Python packages → from requirements
 4. Run this file → python main.py
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from tools import ALL_TOOLS

# ============================================================
# CONFIGURATION
# ============================================================
MODEL_NAME = "qwen3:8b"
AGENT_NAME = "Tenali"

SYSTEM_PROMPT = f"""You are {AGENT_NAME}, an expert coding assistant agent.

When the user gives you a task, follow this workflow:

STEP 1 - ANALYZE: Understand what the user wants. Break it down.
STEP 2 - EXPLORE: Use list_files and read_file to see the project structure and code.
STEP 3 - DETECT: Use detect_project to know what kind of project this is.
STEP 4 - FIX/BUILD: Use write_file to make changes. Write the COMPLETE file content.
STEP 5 - VERIFY: Use run_command to build/test and confirm your changes work.

Rules:
- ALWAYS read a file before editing it. Never guess what's in a file.
- When writing a file, write the ENTIRE file content, not just the changed part.
- After writing changes, run the build or test command to verify.
- If the build fails, read the error, fix it, and try again.
- Explain what you're doing at each step so the user can follow along.
"""

# ============================================================
# STEP 1: Create the LLM and bind tools to it
# ============================================================
llm = ChatOllama(model=MODEL_NAME)
llm_with_tools = llm.bind_tools(ALL_TOOLS)

# ============================================================
# STEP 2: Define the two nodes of our graph
# ============================================================
def agent_node(state: MessagesState) -> dict:
    """The LLM thinks and either answers or requests a tool."""

    # Add system prompt if this is the start of a conversation
    messages = state["messages"]
    if not any(m.type == "system" for m in messages if hasattr(m, "type")):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(ALL_TOOLS)

# ============================================================
# STEP 3: Define the routing logic
# ============================================================
def should_continue(state: MessagesState) -> str:
    """Check if the LLM wants to use a tool or is done."""
    last_message = state["messages"][-1]

    # If the LLM's response has tool_calls, route to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, the LLM is done — end the conversation turn
    return END

# ============================================================
# STEP 4: Build the graph
# ============================================================
graph = StateGraph(MessagesState)

# Add the two nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

# Connect them
graph.add_edge(START, "agent")                                # Start at the agent
graph.add_conditional_edges("agent", should_continue)  # Agent decides: tools or END
graph.add_edge("tools", "agent")                                # After tools, go back to agent

# ============================================================
# STEP 5: Memory
# ============================================================
memory = MemorySaver()

# Compile WITH memory
agent = graph.compile(checkpointer=memory)

# ============================================================
# STEP 6: Chat function and main loop
# ============================================================
def chat(user_message: str, thread_id: str) -> str:
    """Send a message to the agent and get a response."""
    config = {"configurable": {"thread_id": thread_id}}

    final_content =""
    for step in  agent.stream(
        {"messages":[HumanMessage(content=user_message)]},
        stream_mode="updates",
        config=config):

        # We only care about what the 'agent' node is saying/thinking
        if "agent" in step:
            message=step["agent"]["messages"][-1]
            
            # Print the content as it arrives
            if message.content:
                print(f"\n{AGENT_NAME}: {message.content}")
                final_content = message.content
            
            # If the agent is calling a tool, let the user know
            if hasattr(message,"tool_calls") and message.tool_calls:
                for tool in message.tool_calls:
                    print(f"🛠️  [Using Tool: {tool['name']}]")

    return final_content   

def main():
    print("=" * 60)
    print(f" {AGENT_NAME} - Coding Agent (LangGraph)")
    print(f" Model: {MODEL_NAME}")
    print()
    print(" Try commands like:")
    print(' "List all files in ./my_project"')
    print(' "Read main.py and fix any errors"')
    print(' "Create a hello world Python project"')
    print(' "Run the tests and fix failures"')
    print()
    print(" Type 'quit' to exit, 'new' to start fresh conversation")
    print("=" * 60)
    print()

    # Send system prompt as the first message in this thread
    thread_id = "default"
    config = {"configurable": {"thread_id": thread_id}}
    agent.invoke(
        {"messages": [SystemMessage(content=SYSTEM_PROMPT)]},
        config=config,
    )

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print(f"\n{AGENT_NAME}: Goodbye!")
            break
        if user_input.lower() == "new":
            thread_id = f"thread-{id(object())}"
            config = {"configurable": {"thread_id": thread_id}}
            agent.invoke(
                {"messages": [SystemMessage(content=SYSTEM_PROMPT)]},
                config=config,
            )
            print(f"\n{AGENT_NAME}: Fresh conversation started!\n")
            continue

        print()
        response = chat(user_input, thread_id)
        print(f"\n{AGENT_NAME}: {response}\n")

if __name__ == "__main__":
    main()
