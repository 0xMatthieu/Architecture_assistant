import openai
from dotenv import load_dotenv
import os
from smolagents.agents import CodeAgent
from smolagents import GradioUI
from typing import Optional
from smolagents import OpenAIServerModel

load_dotenv()

use_deepseek = False

if use_deepseek:
    model = OpenAIServerModel(
        model_id="deepseek/deepseek-reasoner",
        api_base="https://api.deepseek.com",  # replace with remote open-ai compatible server if necessary
        api_key=os.getenv('DEEPSEEK_API_KEY'),  # replace with API key if necessary
    )
else:
    # Initialize the OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')
    #model = LiteLLMModel(model_id="o1-mini")
    model = OpenAIServerModel(
        model_id="gpt-4o",  # replace with remote open-ai compatible server if necessary
        api_key=os.getenv('OPENAI_API_KEY'),  # replace with API key if necessary
    )

from architecture_agent import managed_architecture_define_agent

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_architecture_define_agent],
    additional_authorized_imports=[],
)

def call_agent(query: str, simple_agent: Optional[bool] = True, ui: Optional[bool] = False):
    if ui:
        GradioUI(manager_agent).launch()

    if simple_agent:
        print(agent.run(query))
    else:
        print(manager_agent.run(query))
