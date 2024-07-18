import os
from tika import parser
import pandas as pd

def parse_resume(file_path):
    parsed = parser.from_file(file_path)
    return parsed['content']

def parse_resumes_in_directory(directory_path):
    resumes = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf") or filename.endswith(".doc") or filename.endswith(".docx"):
            file_path = os.path.join(directory_path, filename)
            resume_text = parse_resume(file_path)
            resumes.append({
                'filename': filename,
                'text': resume_text
            })
    return resumes

def save_parsed_resumes_to_csv(resumes, output_file):
    df = pd.DataFrame(resumes)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    directory_path = "path/to/your/resume/directory"
    output_file = "data/parsed_resumes.csv"
    
    resumes = parse_resumes_in_directory(directory_path)
    save_parsed_resumes_to_csv(resumes, output_file)
    print(f"Parsed resumes saved to {output_file}")
