# Lucidchart Diagram Generator

This project automatically generates Entity-Relationship Diagrams (ERD) and Data Flow Diagrams (DFD) from problem descriptions using OpenAI's GPT-4 and uploads them directly to Lucidchart.

## Features

- Automatic generation of ERD and DFD diagrams
- Direct integration with Lucidchart API
- Support for various entity relationships and data flows
- Automatic browser opening to view the generated diagram
- Customizable shapes, colors, and relationships

## Prerequisites

- Python 3.13 or higher
- OpenAI API key
- Lucidchart API key
- Required Python packages (installed via pyproject.toml)

## Setup

1. Clone this repository
2. Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   LUCIDCHART_API_KEY=your_lucidchart_key_here
   ```
3. Install dependencies:
   ```bash
   pip install .
   ```

## Usage

1. Edit the `problem.txt` file with your system requirements or problem description.

2. Run the generator:
   ```bash
   python generate.py
   ```

3. The script will:
   - Generate appropriate ERD and DFD diagrams
   - Upload them to Lucidchart
   - Automatically open your web browser to view the diagram

4. Once the diagram opens in Lucidchart:
   - Manually adjust the position of entities for better visibility
   - Resize columns and tables as needed
   - Save your changes directly in Lucidchart

## Note

The initial diagram layout is automated but may need manual adjustments in Lucidchart for optimal visualization. Feel free to:
- Drag entities to better positions
- Adjust table column widths
- Modify relationships for clearer connections
- Add additional styling or annotations

## License

MIT License
