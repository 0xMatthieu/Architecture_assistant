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
        model_id="deepseek-reasoner",
        api_base="https://api.deepseek.com",  # replace with remote open-ai compatible server if necessary
        api_key=os.getenv('DEEPSEEK_API_KEY'),  # replace with API key if necessary
    )
else:
    # Initialize the OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')
    #model = LiteLLMModel(model_id="o1-mini")
    model_name = "gpt-4o"
    if model_name == "o3-mini":
        model = OpenAIServerModel(
            model_id="o3-mini",  # replace with remote open-ai compatible server if necessary
            api_key=os.getenv('OPENAI_API_KEY'),  # replace with API key if necessary
            max_completion_tokens=8192
        )
        del model.kwargs["max_tokens"]
    else:
        model = OpenAIServerModel(
            model_id="gpt-4o",  # replace with remote open-ai compatible server if necessary
            api_key=os.getenv('OPENAI_API_KEY'),  # replace with API key if necessary
        )

from architecture_agent import managed_architecture_define_agent
from price_strategy_agent import managed_price_agent

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_architecture_define_agent, managed_price_agent],
    additional_authorized_imports=[],
)

def call_agent(query: str, ui: Optional[bool] = False):
    if ui:
        GradioUI(manager_agent).launch()

    print(manager_agent.run(query, reset=False))
