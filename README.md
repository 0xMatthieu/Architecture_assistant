# Architecture Assistant

This project is designed to help design and promote the best TTControl ECU architecture. It includes tools for reading datasheets, generating reports, and checking architecture requirements.

## Features

- **Read Datasheets**: Extracts content from PDF datasheets.
- **Generate Reports**: Creates PDF or Excel reports based on architecture and price data.
- **Check Requirements**: Validates that all necessary architecture requirements are met.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Architecture_assistant
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add any necessary environment variables.

## Usage

- **Generate a Report**:
  Use the `generate_report` tool to create a report in the desired format.
  ```python
  from price_strategy_agent import generate_report
  report_path = generate_report(Architectures='[...]', format_file='pdf')
  ```

- **Check Architecture Requirements**:
  Use the `check_requirements` tool to ensure all necessary fields are provided.
  ```python
  from architecture_agent import check_requirements
  result = check_requirements(PWM_needed='...', CAN_needed='...', Safety='...')
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
