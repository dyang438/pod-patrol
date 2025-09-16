import asyncio
from agents import Agent, RunConfig, Runner, GuardrailFunctionOutput, RunContextWrapper, output_guardrail
from agent_wrapper import AgentWrapper
from tools import get_pods, describe_pod, get_logs, get_events
from context_manager import ContextManager
from constants import VERIFIER_MODEL

# -------------------------------
# 0. Candidate Answer Agent
# -------------------------------

candidate_answer_agent = Agent(
    name="Assistant", 
    instructions=
    """
    You are an agent who has kubernetes debugging tools at your disposal. You should use the tools to find the current system's context and debug kubernetes clusters that are failing.
    You should automatically try to analyze any pod that debug_kubernetes has a non-healthy status without asking for user input.
    """,
    tools=[get_pods, describe_pod, get_logs, get_events],
)

@output_guardrail
async def verifier_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: str) -> GuardrailFunctionOutput:
    try:
        vote = int(output.strip())
        # Check that vote is either 0 or 1.
        if vote in [0, 1]:
            tripwire = False
        else:
            tripwire = True
    except Exception:
        vote = -1
        tripwire = True
    return GuardrailFunctionOutput(
        output_info={"vote": vote},
        tripwire_triggered=tripwire,
    )

# -------------------------------
# 1. Pod Status Verifier
# -------------------------------

pod_status_verifier = Agent(
    name="Pod Status Verifier",
    instructions="""
    You are an aspect verifier for Kubernetes pod status.
    Use tools to grab pod error context and determine if the input suggestion addresses the observed pod status details.
    Return with only a '1' or '0'. Reply with '1' if it does, and '0' otherwise.
    """,
    tools=[get_pods],
)

# -------------------------------
# 2. Configuration Verifier
# -------------------------------
config_verifier = Agent(
    name="Configuration Verifier",
    instructions="""
    You are an aspect verifier for Kubernetes configuration best practices.
    Use tools to inspect pod configurations and related events, then evaluate whether the input debugging suggestion aligns with recommended configuration practices.
    Return only a '1' if the suggestion is compliant, and '0' otherwise.
    """,
    tools=[describe_pod],
)

# -------------------------------
# 3. Log Analysis Verifier
# -------------------------------
log_analysis_verifier = Agent(
    name="Log Analysis Verifier",
    instructions="""
    You are an aspect verifier specializing in Kubernetes log analysis.
    Use tools to retrieve pod logs and analyze error messages. Determine if the input debugging suggestion addresses the issues indicated in the logs.
    Return only a '1' if it does, and '0' otherwise.
    """,
    tools=[get_logs],
)

# -------------------------------
# 4. Resource/Event Verifier
# -------------------------------
resource_event_verifier = Agent(
    name="Resource/Event Verifier",
    instructions="""
    You are an aspect verifier for Kubernetes resource issues and event anomalies.
    Use tools to collect events and pod status data, then determine if the input debugging suggestion addresses issues such as resource limits, OOM events, or other event-related warnings.
    Return only a '1' if it does, and '0' otherwise.
    """,
    tools=[get_events],
)

# -------------------------------
# Main Pipeline
# -------------------------------

o3_mini_run_config = RunConfig(
    model=VERIFIER_MODEL,
)

async def verify_candidates(question: str, candidate_num: int = 3, canonical_context: ContextManager = None) -> AgentWrapper:
    # 1. Generate candidate answers
    # 2. Verify each candidate answer
    # 3. Aggregate scores
    # 4. Return the best candidate

    hold_evaluations = {}
    hold_agents = {}
    for i in range(candidate_num):
        new_candidate = AgentWrapper(agent=candidate_answer_agent, context_manager=canonical_context)
        await new_candidate.get_response(question)
        await evaluate_using_verifiers(new_candidate)
        hold_evaluations[i] = new_candidate.evaluated
        print(f"Candidate {i} evaluated: {new_candidate.evaluated}")
        hold_agents[i] = new_candidate

    return hold_agents[max(hold_evaluations, key=hold_evaluations.get)]

async def evaluate_using_verifiers(candidate: AgentWrapper):
    pod_result = await Runner.run(pod_status_verifier, candidate.result.final_output, context=candidate.context_manager.get_context(), run_config=o3_mini_run_config)
    config_result = await Runner.run(config_verifier, candidate.result.final_output, context=candidate.context_manager.get_context(), run_config=o3_mini_run_config)
    log_result = await Runner.run(log_analysis_verifier, candidate.result.final_output, context=candidate.context_manager.get_context(), run_config=o3_mini_run_config)
    resource_result = await Runner.run(resource_event_verifier, candidate.result.final_output, context=candidate.context_manager.get_context(), run_config=o3_mini_run_config)
    # Iterate over each verifier result
    total_vote = 0
    denominator = 0
    for name, result in [
        ("Pod Status Verifier", pod_result),
        ("Configuration Verifier", config_result),
        ("Log Analysis Verifier", log_result),
        ("Resource/Event Verifier", resource_result),
    ]:
        try:
            vote = int(result.final_output.strip())
            denominator += 1
        except ValueError as e:
            print(f"Tripwire from {name}: Invalid verifier output: {result.final_output} (error: {e}). Defaulting vote to 0.")
            vote = 0
        total_vote += vote

    candidate.evaluated = total_vote / denominator
