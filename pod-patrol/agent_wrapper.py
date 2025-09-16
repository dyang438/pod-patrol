# File: pod-patrol/agent_wrapper.py

from agents import Agent, Runner, RunConfig
from context_manager import ContextManager
from constants import CANDIDATE_ANSWER_MODEL

starter_run_config = RunConfig(
    model=CANDIDATE_ANSWER_MODEL,
)

"""
This wrapper class is used to wrap an agent and provide a context manager for the agent.
It also provides a last_response attribute to store the last response from the agent.
It also provides a evaluated attribute to store the evaluation of the last response.
"""


class AgentWrapper():
    def __init__(self, agent: Agent, run_config: RunConfig = starter_run_config, context_manager: ContextManager = None):
        self.agent = agent
        self.run_config = run_config
        self.result = ""
        self.context_manager = context_manager or ContextManager()
        self.evaluated = 0

    async def get_response(self, question: str):
        prompt = self.context_manager.get_context()
        self.result = await Runner.run(self.agent, question, run_config=self.run_config, context=prompt)
        self.context_manager.add_user_input(question)
        self.context_manager.add_assistant_response(self.result.final_output)
        candidate_answer = self.result.final_output
        return candidate_answer
