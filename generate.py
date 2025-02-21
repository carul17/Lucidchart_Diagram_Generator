import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from script import *  # Import all functions from script.py

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Read the `script.py` file so OpenAI can "see" available functions
with open("script.py", "r") as f:
    script_code = f.read()

def read_problem_description(file_path):
    """Read the problem description from a text file."""
    with open(file_path, 'r') as file:
        return file.read()

def generate_main_function(description):
    """Ask OpenAI to generate a main function that builds an ERD/DFD using functions from script.py."""
    system_prompt = f"""
    You are an assistant that generates a Python `main()` function to create an Entity-Relationship Diagram (ERD) and Data Flow Diagram (DFD).
    
    You have access to the following functions defined in `script.py`:

    {script_code}

    Use these functions correctly to:
    - Create shapes for entities (use `create_shape`).
    - Define relationships using `create_line`.
    - Generate the Lucidchart JSON (`generate_lucidchart_json`).
    - Upload the diagram to Lucidchart (`import_to_lucidchart`).
    - At the end, **print the Lucidchart link** using the document ID.
    - The script contains a sample main file that you can use as reference as to how the functions can be called.
    - Make sure to add the necessary imports including from script import *

    **Return only valid Python code** for the `main()` function. Do not include explanations. Do not include ``` Python, etc.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": description}
        ]
    )

    return response.choices[0].message.content

def save_and_run_main(main_code):
    """Save the generated main function to a temporary Python file and execute it."""
    with open("generated_main.py", "w") as f:
        f.write(main_code)

    print("🚀 Running generated main function...")
    os.system("python generated_main.py")  # Run the generated file

def main():
    """Main function to read problem description, generate main(), and execute it."""
    problem_description = read_problem_description("problem.txt")
    main_code = generate_main_function(problem_description)

    print("\n🔹 Generated `main()` Function:\n")
    print(main_code)  # Print the generated function

    save_and_run_main(main_code)

if __name__ == "__main__":
    main()
