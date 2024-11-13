import openai
import os
import re
import json
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from typing import Optional
from langchain.output_parsers import PydanticOutputParser


class Resume(BaseModel):
    education: Optional[str] = Field(description="Comma-separated list of educational qualifications")
    skills: Optional[str] = Field(description="Comma-separated Detailed list of skills even the technologies or tools used in some projects & languages known")
    experience: Optional[str] = Field(description="Comma-separated list of work experiences with brief details including years of experience if found")
    courses: Optional[str] = Field(description="Comma-separated list of courses and certificates")
    
    
def clean_json_string(output: str, file_name: str) -> str:
    """
    Removes any leading or trailing characters from the output string
    that are outside the first '{' and last '}', and writes invalid output to a file.

    Args:
        output (str): The raw string that may contain extra characters.
        error_file_path (str): The file path where invalid JSON strings will be stored.

    Returns:
        str: The cleaned string containing only the JSON-like structure.
    """
    # Regular expression to match everything from the first '{' to the last '}'
    match = re.search(r'\{.*\}', output, re.DOTALL)
    
    if match:
        return match.group(0)  # Return the matched JSON-like string
    else:
        error_file_dir = "Error Files"
        file_name = f"{file_name}.txt"

        os.makedirs(error_file_dir, exist_ok=True)  # Create the directory if it doesn't exist
        error_file_path = os.path.join(error_file_dir, file_name)
        
        # Write invalid output to the specified file
        with open(error_file_path, 'w') as error_file:
            error_file.write(output)
        print( f"Invalid JSON written to {error_file_path}")
        return -1
    
def ensure_valid_resume_keys(Resume,input, file_name) -> dict:
    """
    Ensures the cleaned JSON output contains only the valid keys defined in the Resume schema.
    Adds missing keys with a value of None and removes any extra keys.

    Args:
        input (str): A cleaned JSON string that may or may not contain all the valid keys.

    Returns:
        dict: A dictionary with only the valid keys and missing keys added with None.
    """
    # The valid keys according to the Resume schema
    valid_keys = Resume.__fields__.keys()
    
    # Convert the input string to a dictionary
    try:
        resume_dict = json.loads(input)
    except json.JSONDecodeError as e:
        
        print(f"Failed to decode JSON for file {file_name}")
        error_file_dir = "Error Files"
        file_name = f"{file_name}.txt"
        os.makedirs(error_file_dir, exist_ok=True)  # Create the directory if it doesn't exist
        error_file_path = os.path.join(error_file_dir, file_name)
        
        # Write invalid output to the specified file
        with open(error_file_path, 'w') as error_file:
            error_file.write(input)
            
        return -1 
    
    # Create a new dictionary with only the valid keys, and set missing ones to None
    valid_resume_dict = {key: resume_dict.get(key, None) for key in valid_keys}

    return valid_resume_dict

# Function to load the existing processed resumes
def load_processed_resumes(processed_file_path):
    processed_resumes = set()
    if os.path.exists(processed_file_path):
        with open(processed_file_path, "r") as processed_file:
            processed_resumes = set(processed_file.read().splitlines())
    return processed_resumes

# Function to save the processed resume name in the file
def save_processed_resume(processed_file_path, resume_name):
    with open(processed_file_path, "a") as processed_file:
        processed_file.write(resume_name + "\n")

# Function to load structured resumes from the existing JSON file
def load_structured_resumes(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            return json.load(json_file)
    return {}

# Function to save the structured resume in the JSON file without overwriting
def save_structured_resume(json_file_path, resume_name, structured_resume):
    structured_resumes = load_structured_resumes(json_file_path)
    structured_resumes[resume_name] = structured_resume
    with open(json_file_path, "w") as json_file:
        json.dump(structured_resumes, json_file, indent=4)
        
def structure_resumes(directory_path,processed_file_path,json_file_path):
    
    load_dotenv()
    openai.api_key =os.getenv("OPENAI_API_KEY")
    parser = PydanticOutputParser(pydantic_object=Resume)
    prompt = PromptTemplate(
        template="Extract the following information from the resume: {format_instructions}\n{resume_text}",
        input_variables=["resume_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    processed_resumes = load_processed_resumes(processed_file_path) #load the names of the processed resumes
    
    for filename in tqdm(os.listdir(directory_path)):
        resume_name, extension = os.path.splitext(filename)
        
        # Skip the file if it has already been processed
        if resume_name in processed_resumes:
            print(f"Skipping {resume_name} as it has already been processed")
            continue
        
        if extension!=".pdf":
            print(f"Skipping {resume_name} as it is not a PDF file")
            continue
        
        file_path = (f"{directory_path}/{filename}")
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        resume_text = " ".join([page.page_content for page in pages])
        print(f"Read {filename}")
        
        # Create the final prompt by filling in the resume text
        final_prompt = prompt.format(resume_text=resume_text)
        
        try:
            # Call OpenAI's API to get the structured JSON output
            response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  
            prompt=final_prompt,
            max_tokens=1024,  # Adjust based on the expected length
            temperature=0.0
            )
            
            print(f"Completed OpenAi for {filename}")
            
            output=response.choices[0].text
            finish_reason=response.choices[0].finish_reason
            print(f"For file {filename}, the finish reason is {finish_reason}")
            
            cleaned_output=clean_json_string(output, resume_name)
            if cleaned_output!=-1:
                structured_resume = ensure_valid_resume_keys(Resume,cleaned_output, resume_name)
                if structured_resume!=-1:
                    # Save the structured resume to the JSON file
                    save_structured_resume(json_file_path, resume_name, structured_resume)
                    # Add the resume to the processed list
                    save_processed_resume(processed_file_path, resume_name)
        except Exception as e:
            print(f"Failed to Structure the Resume: {e}")
        
        
