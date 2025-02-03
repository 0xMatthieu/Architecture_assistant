from dotenv import load_dotenv
from Utils import read_datasheet_contents, create_price_architecture_report
from smolagents.agents import ToolCallingAgent
from smolagents import tool, ManagedAgent
from typing import Optional, Any
from ai_agent import model
from prompt import MANAGED_AGENT_SHORT_PROMPT
import json

load_dotenv()


class Architecture:
    def __init__(self, Name: str, Reference: str, Number: int, Software: str):
        """
        {
            "Name": "a name or title for this architecture, like '1x TTC 32'",
            "Reference": "the ECU reference, as an example TTC 580",
            "Number": "number of this reference needed to cover the need, shall be a number",
            "Software": "the platform, can only be C, MATCH, Codesys, Qt"
        }
        """
        self.Name = Name
        self.Reference = Reference
        self.Number = Number
        self.Software = Software



@tool
def get_datasheet_content() -> str:
    """
    Returns:

        str: the content of all documents, it is raw data which will be used to define architecture
    """
    content = read_datasheet_contents(folder_path='./Data/Datasheet')
    output = f"""## Documentation is the following {content} \n"""
    return output

@tool
def check_requirements(DO_needed: Optional[str],
                        PWM_needed: Optional[str],
                        CAN_needed: Optional[str],
                        DI_needed: Optional[str],
                        PWD_needed: Optional[str],
                        AI_needed: Optional[str],
                        Safety: Optional[str],
                        Match: Optional[str],
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
        Match: True or False, optional, set to True if missing

    Returns:
        str: the missing information it there is one, else success, mandatory data has been provided
    """
    missing = []
    if not PWM_needed:
        missing.append("PWM_needed")
    if not CAN_needed:
        missing.append("CAN_needed")
    if not Safety:
        missing.append("Safety")
    
    return f"Missing: {', '.join(missing)}" if missing else "All mandatory fields present"


@tool
def format_architecture(architectures: list[Architecture] | dict[str, Architecture]) -> dict[str, str | Any]:
    """
    Check if a single architecture fits all information needed

    Args:
        Architectures: an instance of Architecture class containing name, reference, number and software needed

    Returns:
        missing_info: the missing information it there is one, else success, mandatory data has been provided
        data: updated Architectures in JSON format with only mandatory fields
    """
    missing_info = []
    data_updated = False
    if isinstance(architectures, dict):
        architectures = list(architectures.values())

    data = []
    for arch in architectures:
        data.append({
            "Name": arch.Name,
            "Reference": arch.Reference,
            "Number": arch.Number,
            "Software": arch.Software
        })
    required_fields = {"Name", "Reference", "Number", "Software"}
    for architecture in data:
        # Remove unnecessary fields
        keys_to_remove = set(architecture.keys()) - required_fields
        for key in keys_to_remove:
            del architecture[key]
            data_updated = True
        missing = []
        if not architecture.get("Name"):
            missing.append("Name")
        if not architecture.get("Reference"):
            missing.append("Reference")
        if not architecture.get("Number"):
            missing.append("Number")
        if not architecture.get("Software"):
            missing.append("Software")
        
        if missing:
            missing_info.append(f"Architecture {architecture.get('Name', 'Unnamed')}: Missing {', '.join(missing)}")

    return {
        "missing_info": "\n".join(missing_info) if missing_info else "All mandatory fields present",
        "data": data if data_updated else Architectures
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
3: define best solutions, provide 3 solutions in JSON format and check that all arguments have been provided

As soon as you have a JSON list with 3 solutions, you can return this list in JSON format

below is an example of expected output

{"Architecture":[
    {
        "Name": "2x TTC 32",
        "Reference": "TTC 32",
        "Number": "2",
        "Software": "Codesys"
    },
    {
        "Name": "1x TTC 580",
        "Reference": "TTC 580",
        "Number": "1",
        "Software": "MATCH"
    }
]}
"""
)
