from dotenv import load_dotenv
from Utils import read_datasheet_contents, create_price_architecture_report
from smolagents.agents import ToolCallingAgent
from smolagents import tool, ManagedAgent
from typing import Optional
from ai_agent import model

load_dotenv()

@tool
def get_price_list() -> str:
    """
    Returns:
    str: the content of all references and prices
    """
    content = read_datasheet_contents(folder_path='./Data/Price')
    output = f"""## Price list is the following {content} \n"""
    return output

@tool
def generate_report(format: str = 'pdf') -> str:
    """
    Generates a report in the specified format (pdf or excel) containing price and architecture information.

    Args:
    format (str): The format of the report, either 'pdf' or 'excel'.

    Returns:
    str: The path to the generated report file.
    """
    try:
        report_path = create_price_architecture_report(output_format=format)
        return f"Report generated successfully: {report_path}"
    except Exception as e:
        return f"Failed to generate report: {e}"


agent = ToolCallingAgent(tools=[get_price_list], model=model)

managed_price_agent = ManagedAgent(
    agent=agent,
    name="price_strategy_designer",
    description="""You will be tasked to help design and promote the best TTControl ECU offer""",
    additional_prompting ="""You can get all prices, and provide feedback with all references / price / quantity
    """
)


