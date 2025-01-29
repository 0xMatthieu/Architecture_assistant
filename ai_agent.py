import openai
from dotenv import load_dotenv
import os
from Utils import read_datasheet_contents

load_dotenv()
from smolagents.agents import ToolCallingAgent, CodeAgent
from smolagents import tool, ManagedAgent
from typing import Optional

use_deepseek = True

if use_deepseek:
    from smolagents import OpenAIServerModel
    model = OpenAIServerModel(
        model_id="deepseek/deepseek-reasoner",
        api_base="https://api.deepseek.com",  # replace with remote open-ai compatible server if necessary
        api_key=os.getenv('DEEPSEEK_API_KEY'),  # replace with API key if necessary
    )
else:
    from smolagents import LiteLLMModel
    os.environ['LITELLM_LOG'] = 'DEBUG'
    # Initialize the OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')
    model = LiteLLMModel(model_id="gpt-4o")

@tool
def get_datasheet_content() -> str:
    """
    Returns:
    str: the content of all documents, which will be used to define architecture
    """
    content = read_datasheet_contents()
    output = f"""## Documentation is the following {content} \n"""
    return output

@tool
def check_requirements(DO_needed: Optional[str],
                        PWM_needed: Optional[str],
                        CAN_needed: Optional[str],
                        DI_needed: Optional[str],
                        PWD_needed: Optional[str],
                        AI_needed: Optional[str],
                        Safety: Optional[str]
                        ) -> str:
    """
    Check if all requirements are there, if it is optional it can be skipped

    Args:
        information about requested architecture, best is to provide the following:
        DO_needed: number of digital outputs (DO), optional
        PWM_needed: number of proportional outputs (PWM), mandatory
        CAN_needed: number of CAN channels, mandatory
        DI_needed: number of digital inputs (DI), optional
        PWD_needed: number of frequency inputs (PWD), optional
        AI_needed: number of analog inputs (AI), optional
        Safety: True or False, mandatory

    Returns:
        str: the missing information it there is one
    """


agent = ToolCallingAgent(tools=[get_datasheet_content, check_requirements], model=model)

managed_architecture_define_agent = ManagedAgent(
    agent=agent,
    name="assistant",
    description="""You will be tasked to help design and promote the best ECU architecture""",
    additional_prompting ="""You can use following documents to better know the product portfolio and based your answer.
    To work you need to know at least the number of outputs, CAN as well as the software used to develop.
    First you need to check you have enough information to answer, if no, ask the user to provide them
    If there is more than one possibility, limit your answer to 3 solutions which shall be different.
    Few examples below, answer using JSON format
    Example 1
    {
        "Input": 11 AI + 7 DO + 1 PWM, 3 CAN, Codesys,
            "Output": [
            {
              "Solution": "1x HY-TTC 32",
              "Programming": "Codesys"
            }
        ]
    }
    Example 2
    Input: 21 AI + 7 DO + 16 PWM, C or Codesys
    Output: 1x TTC510 Codesys or 1x TTC2310 in C or 3x TTC 2038 in C
        {
        "Input": 21 AI + 7 DO + 16 PWM, C or Codesys
            "Output": [
            {
              "Solution": "1x HY-TTC 510",
              "Programming": "Codesys"
            },
            {
              "Solution": "1x TTC 2310 (TTC 2785 variant)",
              "Programming": "C"
            },
            {
              "Solution": "2x TTC 32",
              "Programming": "Codesys"
            }
        ]
    }
    """
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_architecture_define_agent],
    additional_authorized_imports=[],
)

def call_agent(query: str, simple_agent: Optional[bool] = True):
    if simple_agent:
        print(agent.run(query))
    else:
        print(manager_agent.run(query))