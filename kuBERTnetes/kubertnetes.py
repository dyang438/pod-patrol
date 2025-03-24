# File: kubertnetes/kubertnetes.py

from tap import Tap
from gpt_wrapper import agent_wrapper

class kubertnetes_inputs(Tap):
    question: str = ""

async def main():
    inputs = kubertnetes_inputs().parse_args()
    agent = agent_wrapper()
    while True:
        if inputs.question == "":
            inputs.question = input("Solve your kubernetes problem here:\n> ")
        else:
            print("You inputted question:\n" + "> " + inputs.question)

        # Grab Response here:
        response = await agent.get_response(inputs.question)
        print(response)

        """
        Flow:
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

        # TODO:


        inputs.question = ""
    


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())