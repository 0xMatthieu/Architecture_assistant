from dotenv import load_dotenv
from Utils import read_datasheet_contents, create_price_architecture_report, read_excel_page
from smolagents.agents import ToolCallingAgent
from smolagents import tool, ManagedAgent
from typing import Optional
from ai_agent import model
from architecture_agent import format_architecture
from prompt import MANAGED_AGENT_SHORT_PROMPT
import json

load_dotenv()

QUANTITY_SINGLE_UNIT = "Quantity single unit"
PRICE_SINGLE_UNIT = "Price single unit"
QUANTITY_BOX = "Quantity box"
PRICE_BOX = "Price box"
QUANTITY_PALETTE = "Quantity palette"
PRICE_PALETTE = "Price palette"


@tool
def get_price_list(architectures: list[dict]) -> list[dict]:
    """
    get price list and fill a list based on given architectures

    Args:
        architectures: a list of dict containing
        {
            "name": "a name or title for this architecture, like '1x TTC 32'",
            "reference": "the ECU reference, as an example TTC 580",
            "number": "number of this reference needed to cover the need, shall be a number",
            "software": "the platform, can only be C, MATCH, Codesys, Qt"
        }

    Returns:
        ecu_price: a list of all ECU and prices
            {
                "reference": "the ECU reference, for example TTC 580",
                "designation": "the ECU reference, for example HY-TTC 580-CD",
                "article_number": "the ECU reference, for example 927891",
                "quantity_single_unit": "the MOQ for a single unit",
                "price_single_unit": "the price for a single unit"
                "quantity_box": "the MOQ for a box",
                "price_box": "the price for a box"
                "quantity_palette": "the MOQ for a palette",
                "price_palette": "the price for a palette"
            }
    """
    df = read_excel_page(folder_path='./Data/Test', sheet_number=1)
    ecu_price_list = []

    for architecture in architectures:
        ref = architecture.get("reference")
        software = architecture.get("software")

        # Check if the reference and software match a line in the DataFrame
        match = df[(df['Reference'] == ref) & (df['Software'] == software)]
        if not match.empty:
            for _, row in match.iterrows():
                ecu_price_list.append({
                    "reference": row["Reference"],
                    "designation": row["Designation"],
                    "article_number": row["Article number"],
                    "quantity_single_unit": row[QUANTITY_SINGLE_UNIT],
                    "price_single_unit": row[PRICE_SINGLE_UNIT],
                    "quantity_box": row[QUANTITY_BOX],
                    "price_box": row[PRICE_BOX],
                    "quantity_palette": row[QUANTITY_PALETTE],
                    "price_palette": row[PRICE_PALETTE]
                })

    return ecu_price_list

@tool
def generate_report(architectures: list[dict], format_file: str = 'pdf') -> str:
    """
    Generates a report in the specified format (pdf or excel) containing price and architecture information.

    Args:
        architectures: a list of all ECU and prices
            {
                "reference": "the ECU reference, for example TTC 580",
                "designation": "the ECU reference, for example HY-TTC 580-CD",
                "article_number": "the ECU reference, for example 927891",
                "quantity_single_unit": "the MOQ for a single unit",
                "price_single_unit": "the price for a single unit"
                "quantity_box": "the MOQ for a box",
                "price_box": "the price for a box"
                "quantity_palette": "the MOQ for a palette",
                "price_palette": "the price for a palette"
            }

        format_file: The format of the report, either 'pdf' or 'excel'.

    Returns:
        str: The path to the generated report file.
    """
    try:

        missing_info = []
        data = architectures
        required_fields = {"reference", "designation", "article_number", "quantity_single_unit", "price_single_unit"}
        for architecture in data:
            missing = []
            if not architecture.get("reference"):
                missing.append("reference")
            if not architecture.get("designation"):
                missing.append("designation")
            if not architecture.get("article_number"):
                missing.append("article_number")
            if not architecture.get("quantity_single_unit"):
                missing.append("quantity_single_unit")
            if not architecture.get("price_single_unit"):
                missing.append("price_single_unit")

            if missing:
                missing_info.append(f"Architecture {architecture.get('name', 'Unnamed')}: Missing {', '.join(missing)}")

        if missing_info:
            return "\n".join(missing_info)

        report_path = create_price_architecture_report(data, output_format=format_file)
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


