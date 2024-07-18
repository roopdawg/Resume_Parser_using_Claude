import anthropic

claude_client = anthropic.Anthropic(api_key="your_anthropic_api_key")
claude_model = "claude-3-haiku-20240307"

def extract_match_criteria(match_results, job_description_text, candidate_query_text=None):
    if candidate_query_text:
        context_type = 'candidate_query'
        prompt = f"""
        Based on the following candidate query and match results, identify the specific criteria (skills, job titles, experience, education, and specific requirements) that were met.

        Candidate Query:
        {candidate_query_text}

        Job Description:
        {job_description_text}

        Match Results:
        {match_results}

        Output:
        {{
          "Matched Skills": [List of Matched Skills],
          "Matched Job Titles": [List of Matched Job Titles],
          "Matched Experience": [List of Matched Experience],
          "Matched Education": [List of Matched Education],
          "Matched Specific Requirements": [List of Matched Specific Requirements]
        }}
        """
    else:
        context_type = 'job_description'
        prompt = f"""
        Based on the following job description and match results, identify the specific criteria (skills, job titles, experience, education, and specific requirements) that were met.

        Job Description:
        {job_description_text}

        Match Results:
        {match_results}

        Output:
        {{
          "Matched Skills": [List of Matched Skills],
          "Matched Job Titles": [List of Matched Job Titles],
          "Matched Experience": [List of Matched Experience],
          "Matched Education": [List of Matched Education],
          "Matched Specific Requirements": [List of Matched Specific Requirements]
        }}
        """
    
    response = claude_client.completions.create(
        model=claude_model,
        prompt=prompt,
        max_tokens=500
    )
    return response["completion"]

if __name__ == "__main__":
    match_results = "Example match results from FAISS and BM25 here."
    job_description_text = "Example job description text here."
    candidate_query_text = "Looking for a Senior Software Engineer with 5+ years of Python experience."
    
    criteria = extract_match_criteria(match_results, job_description_text, candidate_query_text)
    print(criteria)
