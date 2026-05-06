import os
import subprocess
from langchain_core.tools import tool
from langchain_community.agent_toolkits import FileManagementToolkit

# ============================================================
# BUILT-IN FILE TOOLS (from LangChain)
# ============================================================
# FileManagementToolkit provides a suite of 6 tools for file operations.
# root_dir="." ensures the agent stays within the current directory.
file_toolkit = FileManagementToolkit(root_dir=".")
file_tools = file_toolkit.get_tools()

# ============================================================
# CUSTOM TOOL: DETECT PROJECT
# ============================================================
@tool
def detect_project(directory: str) -> str:
    """
    Detect the project type and available build/run commands.
    Use this to figure out how to build, test, or run the project.
    """
    try:
        # Clean up the directory string from any extra whitespace or quotes
        directory = directory.strip().strip("\"'")
        files = os.listdir(directory)
        info = []

        # Logic to identify the tech stack based on configuration files
        if "package.json" in files:
            info.append("Type: Node.js / JavaScript project")
            info.append("Install: npm install")
            info.append("Build: npm run build")
            info.append("Test: npm test")
            info.append("Run: npm start")
            pkg_path = os.path.join(directory, "package.json")
            with open(pkg_path, "r") as f:
                content = f.read(3000)
            info.append(f"\npackage.json snippet:\n{content}")

        elif "requirements.txt" in files:
            info.append("Type: Python project")
            info.append("Install: pip install -r requirements.txt")
            info.append("Run: python main.py")
            info.append("Test: pytest")

        elif "pyproject.toml" in files:
            info.append("Type: Python project (modern)")
            info.append("Install: pip install -e .")
            info.append("Test: pytest")

        elif "Cargo.toml" in files:
            info.append("Type: Rust project")
            info.append("Build: cargo build")
            info.append("Run: cargo run")
            info.append("Test: cargo test")

        elif "go.mod" in files:
            info.append("Type: Go project")
            info.append("Build: go build")
            info.append("Run: go run .")
            info.append("Test: go test ./...")

        elif "pom.xml" in files:
            info.append("Type: Java / Maven project")
            info.append("Build: mvn package")
            info.append("Test: mvn test")

        else:
            info.append("Type: Unknown — no recognized config files found")
            info.append(f"Files present: {', '.join(files[:20])}")

        return "\n".join(info)
    except Exception as e:
        return f"Error detecting project: {e}"

# ============================================================
# CUSTOM TOOL: RUN COMMAND
# ============================================================
@tool
def run_command(command: str) -> str:
    """
    Run a shell command (build, test, lint, etc.) and return the output.
    Examples: 'npm run build', 'python -m pytest', 'cargo test'
    """
    try:
        # Executes the command in the system shell
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60, # Prevent infinite loops/hangs
            cwd=os.getcwd(),
        )
        
        output = ""
        # Capture standard output (last 3000 chars to avoid token limits)
        if result.stdout:
            output += f"STDOUT:\n{result.stdout[-3000:]}\n"
        # Capture error output
        if result.stderr:
            output += f"STDERR:\n{result.stderr[-3000:]}\n"
        
        output += f"Exit code: {result.returncode}"
        output += " (SUCCESS)" if result.returncode == 0 else " (FAILED)"
        
        return output if output.strip() else "Command completed with no output."
    
    except subprocess.TimeoutExpired:
        return "Command timed out after 60 seconds."
    except Exception as e:
        return f"Error running command: {e}"

# ============================================================
# TOOL AGGREGATION
# ============================================================
# Combine the 6 file tools and the 2 custom tools into one list
ALL_TOOLS = file_tools + [detect_project, run_command]