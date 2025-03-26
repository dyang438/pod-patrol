# File: kubertnetes/kubertnetes.py

from tap import Tap
from agent_wrapper import AgentWrapper
from context_manager import ContextManager
import asyncio
from judge_agent import verify_candidates, candidate_answer_agent

class KubertnetesInputs(Tap):
    question: str = ""
    validate_solution: bool = False
    candidate_num: int = 3

async def main():
    inputs = KubertnetesInputs().parse_args()
    starting_agent = AgentWrapper(candidate_answer_agent)
    canonical_context = ContextManager()
    while (1):
        if inputs.question == "":
            inputs.question = input("\n> ")
        else:
            print("You inputted question:\n" + "> " + inputs.question)

        # Grab Response here:
        if inputs.question == "quit":
            break
        if inputs.validate_solution:
            print("Validating solution...")
            canonical_agent = await verify_candidates(inputs.question, inputs.candidate_num, canonical_context)
            # Update canonical context
            canonical_context = canonical_agent.context_manager
            print("\n\n" + canonical_agent.result.final_output)
        else:
            response = await starting_agent.get_response(inputs.question)
            print(response)

        """
        Ideal Flow:
        1. Get question from user input or command line args 
        1a. Santize/validate question
        2. Pass question to agent wrapper which handles LLM interaction
        3. Call required tools here
        3a. Validate tool call arguments
        4. Ask agent to use context from tools to answer question
        4a. Retain for multi-line context
        4b. Post-process tool call results
        5. Print response
        6. Reset question and continue loop
        """

        inputs.question = ""
    
    print("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())