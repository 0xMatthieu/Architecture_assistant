from Utils import read_datasheet_contents, read_excel_page
from smolagents.agents import ToolCallingAgent
from smolagents import tool, ManagedAgent
from typing import Optional, Any
from ai_agent import model
from prompt import MANAGED_AGENT_SHORT_PROMPT

@tool
def get_datasheet_content() -> str:
    """
    Returns:

        str: the content of all documents, it is raw data which will be used to define architecture
    """
    return read_excel_page(folder_path='./Data/Test', sheet_number=0)

@tool
def check_requirements(requirements: dict) -> str:
    """
    Check if all requirements are there, if it is optional it can be skipped

    Args:
        requirements: a dict containing
        {
            information about requested architecture, best is to provide the following:
            DO_needed: number of digital outputs (DO), optional
            PWM_needed: number of proportional outputs (PWM), mandatory
            CAN_needed: number of CAN channels, mandatory
            DI_needed: number of digital inputs (DI), optional
            PWD_needed: number of frequency inputs (PWD), optional
            AI_needed: number of analog inputs (AI), optional
            Safety: True or False, mandatory
            Match: True or False, optional, set to True if missing
        }

    Returns:
        str: the missing information it there is one, else success, mandatory data has been provided
    """
    missing = []
    if not requirements.get("PWM_needed"):
        missing.append("PWM_needed")
    if not requirements.get("CAN_needed"):
        missing.append("CAN_needed")
    if not requirements.get("Safety"):
        missing.append("Safety")
    
    return f"Missing: {', '.join(missing)}" if missing else "All mandatory fields present"


@tool
def format_architecture(architectures: list[dict]) -> dict[str, list[dict] | Any]:
    """
    Check if a single architecture fits all information needed

    Args:
        architectures: a list of dict containing
        {
            "name": "a name or title for this architecture, like '1x TTC 32'",
            "reference": "the ECU reference, as an example TTC 580",
            "number": "number of this reference needed to cover the need, shall be a number",
            "software": "the platform, can only be C, MATCH, Codesys, Qt"
        }

    Returns:
        missing_info: the missing information it there is one, else success, mandatory data has been provided
        architectures: updated dict with only mandatory fields, same as input if missing_info is empty
    """

    missing_info = []
    data_updated = False

    required_fields = {"name", "reference", "number", "software"}
    for i, architecture in enumerate(architectures):
        # Remove unnecessary fields
        keys_to_remove = set(architecture.keys()) - required_fields
        for key in keys_to_remove:
            del architecture[key]
            data_updated = True
        missing = []
        if not architecture.get("name"):
            missing.append("name")
        if not architecture.get("reference"):
            missing.append("reference")
        if not architecture.get("number"):
            missing.append("number")
        if not architecture.get("software"):
            missing.append("software")
        
        if missing:
            missing_info.append(f"Architecture {architecture.get('name', 'Unnamed')}: Missing {', '.join(missing)}")

    return {
        "missing_info": "\n".join(missing_info) if missing_info else "All mandatory fields present",
        "architectures": architectures
    }

agent = ToolCallingAgent(tools=[get_datasheet_content, check_requirements, format_architecture], model=model)

managed_architecture_define_agent = ManagedAgent(
    agent=agent,
    name="architecture_designer",
    description="""You will be tasked to help design and promote the best TTControl ECU architecture""",
    managed_agent_prompt=MANAGED_AGENT_SHORT_PROMPT,
    additional_prompting ="""You have to follow this steps to define the better solution:
1: check if there is no missing arguments, you have to have enough information
2: get all technical information like datasheet and all documentation to better know the ECU product portfolio
3: define best solutions, provide 3 solutions in architecture class and check that all arguments have been provided

As soon as you have a list with 3 solutions, you can return this list.
"""
)


