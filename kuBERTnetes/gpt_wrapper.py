# File: kubertnetes/gpt_wrapper.py

from agents import Agent, Runner, RunConfig
from tools import debug_kubernetes

# agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# starter_run_config = RunConfig(
#     model="gpt-4o-mini",
# )

# result = Runner.run_sync(agent, "Write a haiku about recursion in math.", run_config=starter_run_config)
# print(result.final_output)


starter_agent = Agent(
    name="Assistant", 
    instructions=
    """
    You are an agent who has kubernetes debugging tools at your disposal. You should use the tools to find the current system's context and debug kubernetes clusters that are failing.
    """,
    tools=[debug_kubernetes],
)

starter_run_config = RunConfig(
    model="gpt-4o-mini",
)

class agent_wrapper():
    def __init__(self, agent: Agent = starter_agent, run_config: RunConfig = starter_run_config):
        self.agent = agent
        self.run_config = run_config
        self.result = ""

    async def get_response(self, question: str):
        self.result = await Runner.run(self.agent, question, run_config=self.run_config)
        return self.result.final_output