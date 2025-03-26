# File: kubertnetes/tools.py

import subprocess
from agents import function_tool
from context_manager import ContextManager

# Example usage:
# output = run_command("kubectl get pods -l app=faulty-app")
# print("Command output:", output)

# -------------------------------
# Tool 1: Get Pods
# -------------------------------
@function_tool(
    name_override="K8s_Get_Pods",
    description_override="Lists all pods in the specified namespace (defaults to 'default')."
)
def get_pods(namespace: str) -> str:
    print('running get_pods')
    try:
        cmd = f"kubectl get pods -n {namespace}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return f"Command error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {e}"

# -------------------------------
# Tool 2: Describe Pod
# -------------------------------
@function_tool(
    name_override="K8s_Describe_Pod",
    description_override="Shows details for a specific pod in the specified namespace (defaults to 'default'). Requires 'pod_name'."
)
def describe_pod(pod_name: str, namespace: str) -> str:
    print('running describe_pod')
    if not pod_name:
        return "Error: 'pod_name' is required for action 'describe_pods'."
    try:
        cmd = f"kubectl describe pod {pod_name} -n {namespace}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return f"Command error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {e}"

# -------------------------------
# Tool 3: Get Logs
# -------------------------------
@function_tool(
    name_override="K8s_Get_Logs",
    description_override="Fetches logs for a specific pod in the specified namespace (defaults to 'default'). Requires 'pod_name'."
)
def get_logs(pod_name: str, namespace: str) -> str:
    print('running get_logs')
    if not pod_name:
        return "Error: 'pod_name' is required for action 'get_logs'."
    try:
        cmd = f"kubectl logs {pod_name} -n {namespace}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return f"Command error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {e}"

# -------------------------------
# Tool 4: Get Events
# -------------------------------
@function_tool(
    name_override="K8s_Get_Events",
    description_override="Lists events in the specified namespace. Can default to 'default' if not specified."
)
def get_events(namespace: str) -> str:
    print('running get_events')
    try:
        cmd = f"kubectl get events -n {namespace}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return f"Command error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {e}"

# -------------------------------
# Helper function to process pod names (optional)
# -------------------------------
# def process_pod_names(output: str):
#     lines = output.splitlines()
#     if len(lines) > 1:
#         # Assume the first line is a header.
#         for line in lines[1:]:
#             print("line: " + line)
#             columns = line.split()
#             if len(columns) >= 5:
#                 pod_name = columns[0]
#                 ready = columns[1]
#                 status = columns[2]
#                 restarts = columns[3]
#                 age = columns[4]