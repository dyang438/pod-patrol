# File: kubertnetes/tools.py

import subprocess
from agents import function_tool

# Example usage:
# output = run_command("kubectl get pods -l app=faulty-app")
# print("Command output:", output)

def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {e}"

@function_tool(
    name_override="Kubernetes_Debug_Tool",
    description_override=(
        "A tool for debugging Kubernetes clusters. Supports actions: 'get_pods', "
        "'describe_pods', 'get_logs', and 'get_events'. Specify 'pod_name' for actions "
        "that require it (like 'describe_pods' or 'get_logs'). 'namespace' defaults to 'default'."
    ),
)
def debug_kubernetes(
    action: str, 
    pod_name: str,
    namespace: str,
) -> str:
    """
    Debugs a Kubernetes cluster by running specific kubectl commands.

    Parameters:
    - action (str): The debugging action to perform. Options are:
        - "get_pods": List all pods in the given namespace.
        - "describe_pods": Show details for a specific pod (requires pod_name).
        - "get_logs": Fetch logs from a specific pod (requires pod_name).
        - "get_events": List events in the given namespace.
    - pod_name (str, optional): The name of the pod to inspect (if needed).
    - namespace (str, optional): The Kubernetes namespace to target (default "default").

    Returns:
    - str: The output from the kubectl command or an error message if execution fails.
    """
    if namespace is None:
        namespace = "default"
    if pod_name is None:
        pod_name = ""
    try:
        match action:
            case "get_pods":
                cmd = f"kubectl get pods -n {namespace}"
            case "describe_pods":
                if not pod_name:
                    return "Error: 'pod_name' is required for action 'describe_pods'."
                cmd = f"kubectl describe pod {pod_name} -n {namespace}"
            case "get_logs":
                if not pod_name:
                    return "Error: 'pod_name' is required for action 'get_logs'."
                cmd = f"kubectl logs {pod_name} -n {namespace}"
            case "get_events":
                cmd = f"kubectl get events -n {namespace}"
            case _:
                return (
                    f"Error: Unknown action '{action}'. Supported actions: "
                    "get_pods, describe_pods, get_logs, get_events."
                )
        
        # Run the command and capture its output.
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return f"Command error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {e}"