from dotenv import load_dotenv
from Utils import read_datasheet_contents, create_price_architecture_report
from smolagents.agents import ToolCallingAgent
from smolagents import tool, ManagedAgent
from typing import Optional
from ai_agent import model
from architecture_agent import format_architecture
from prompt import MANAGED_AGENT_SHORT_PROMPT
import json

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
def generate_report(architectures: list[dict], format_file: str = 'pdf') -> str:
    """
    Generates a report in the specified format (pdf or excel) containing price and architecture information.

    Args:
        Architectures: a list of all ECU and prices
            {
                "Reference": "the ECU reference, for example TTC 580",
                "Designation": "the ECU reference, for example HY-TTC 580-CD",
                "Article_number": "the ECU reference, for example 927891",
                "Quantity": "a list with requested quantities, for example [1, 20, 100]",
                "Price": "the prices found in list, for example [500, 400, 300]"
            }

        format_file: The format of the report, either 'pdf' or 'excel'.

    Returns:
        str: The path to the generated report file.
    """
    try:

        missing_info = []
        data = json.loads(architectures)
        required_fields = {"Reference", "Designation", "Article_number", "Quantity", "Price"}
        for architecture in data:
            missing = []
            if not architecture.get("Reference"):
                missing.append("Reference")
            if not architecture.get("Designation"):
                missing.append("Designation")
            if not architecture.get("Article_number"):
                missing.append("Article_number")
            if not architecture.get("Quantity"):
                missing.append("Quantity")
            if not architecture.get("Price"):
                missing.append("Price")

            if missing:
                missing_info.append(f"Architecture {architecture.get('Name', 'Unnamed')}: Missing {', '.join(missing)}")

        if missing_info:
            return "\n".join(missing_info)

        report_path = create_price_architecture_report(Architectures, output_format=format_file)
        return f"Report generated successfully: {report_path}"
    except Exception as e:
        return f"Failed to generate report: {e}"


agent = ToolCallingAgent(tools=[get_price_list, generate_report, format_architecture], model=model)

managed_price_agent = ManagedAgent(
    agent=agent,
    name="price_strategy_designer",
    managed_agent_prompt=MANAGED_AGENT_SHORT_PROMPT,
    description="""You will be tasked to help design and promote the best TTControl ECU offer""",
    additional_prompting ="""You have to follow this steps to define the better solution:
        1: if there is already some architecture required, format them to get a JSON with all architecture
        2: get all prices
        3: create the report
    """
)


