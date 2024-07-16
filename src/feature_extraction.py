import anthropic

claude_client = anthropic.Anthropic(api_key="your_anthropic_api_key")
claude_model = "claude-3-haiku-20240307"

def extract_features_with_claude(text, context_type):
    prompt = f"""
    Extract all the skills, job titles, experience, education, and specific requirements from the following {context_type} text.

    {context_type} Text:
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
    response = claude_client.completions.create(
        model=claude_model,
        prompt=prompt,
        max_tokens=300
    )
    return response["completion"]


