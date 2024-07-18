import anthropic

claude_client = anthropic.Anthropic(api_key="your_anthropic_api_key")
claude_model = "claude-3-haiku-20240307"

def extract_features_with_claude(text, context_type):
    if context_type == 'job_description':
        prompt = f"""
        Extract all the skills, job titles, experience, education, and specific requirements from the following job description text.

        Job Description Text:
        {text}

        Output:
        {{
          "Skills": [List of Skills],
          "Job Titles": [List of Job Titles],
          "Experience": [List of Experience],
          "Education": [List of Education],
          "Specific Requirements": [List of Specific Requirements]
        }}
        """
    elif context_type == 'candidate_query':
        prompt = f"""
        Based on the following natural language query, provide a structured candidate profile with the required skills, job titles, experience, education, and specific requirements.

        Candidate Query:
        {text}

        Output:
        {{
          "Skills": [List of Skills],
          "Job Titles": [List of Job Titles],
          "Experience": [List of Experience],
          "Education": [List of Education],
          "Specific Requirements": [List of Specific Requirements]
        }}
        """
    else:
        raise ValueError("Invalid context_type. Must be 'job_description' or 'candidate_query'.")

    response = claude_client.completions.create(
        model=claude_model,
        prompt=prompt,
        max_tokens=300
    )
    return response["completion"]
