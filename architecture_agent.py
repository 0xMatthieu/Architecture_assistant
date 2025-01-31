from dotenv import load_dotenv
from Utils import read_datasheet_contents
from smolagents.agents import ToolCallingAgent
from smolagents import tool, ManagedAgent
from typing import Optional
from ai_agent import model

load_dotenv()

@tool
def get_datasheet_content() -> str:
    """
    Returns:

        str: the content of all documents, which will be used to define architecture
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
    # Temporary implementation to avoid syntax errors
    missing = []
    if not PWM_needed:
        missing.append("PWM_needed")
    if not CAN_needed:
        missing.append("CAN_needed")
    if not Safety:
        missing.append("Safety")
    
    return f"Missing: {', '.join(missing)}" if missing else "All mandatory fields present"


@tool
def check_architecture_requirements(Architectures: str) -> str:
    """
    Check if a single architecture fits all information needed

    Args:
        Architectures: a list of all architectures found, shall follow the following structure
            {[{Name: a name or title for this architecture, like "1x TTC 32"},
            {Reference: the ECU reference, as an example TTC 580},
            {Number: number of this reference needed to cover the need, shall be a number},
            {Software: the platform, can only be C, MATCH, Codesys, Qt}]}

    Returns:
        str: the missing information it there is one, else success, mandatory data has been provided
    """
    # Temporary implementation to avoid syntax errors
    missing = []
    for Architecture in Architectures:
        if not Reference:
            missing.append("Reference")
        if not Number:
            missing.append("Number")
        if not Software:
            missing.append("Software")

    return f"Missing: {', '.join(missing)}" if missing else "All mandatory fields present"

agent = ToolCallingAgent(tools=[get_datasheet_content, check_requirements, check_architecture_requirements], model=model)

managed_architecture_define_agent = ManagedAgent(
    agent=agent,
    name="architecture_designer",
    description="""You will be tasked to help design and promote the best TTControl ECU architecture""",
    additional_prompting ="""You can use following documents to better know the product portfolio and based your answer.
    To work you need to know at least the number of outputs, CAN as well as the software used to develop.
    First you need to check you have enough information to answer, if no, ask the user to provide them
    Next define the best TTControl ECU architecture
    If there is more than one possibility, limit your answer to 3 solutions which shall be different.
    Few examples below, answer using JSON format
    Example 1
    {
        "Input": 11 AI + 7 DO + 1 PWM, 3 CAN, Codesys,
            "Output": [
            {
              "Reference": "HY-TTC 32",
              "Number": "1",
              "Programming": "Codesys"
            }
        ]
    }
    Example 2
    {
    "Input": 21 AI + 7 DO + 16 PWM, C or Codesys
        "Output": [
        {
          "Reference": "1x HY-TTC 510",
          "Number": "1",
          "Software": "Codesys"
        },
        {
          "Reference": "1x TTC 2310 (TTC 2785 variant)",
          "Number": "1",
          "Software": "C"
        },
        {
          "Reference": "2x TTC 32",
          "Number": "2",
          "Software": "Codesys"
        }
        ]
    }
    """
)


