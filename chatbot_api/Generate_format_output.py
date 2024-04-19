from openai import OpenAI
import json

def format_response(query):
    client = OpenAI()
    
    prompt = """
    You are an enthusiastic assistant who likes helping others
    Objective:  Style and format the generated response for better readability and presentation while preserving the original content.

    Heading Formatting:
    Start each section with a heading in bold font.
    Use H3 for main heading & H5 for sub-heading.
    
    Tabular Format:
    Whenever there's tabular data present in the response, represent it in a structured table format.
    Ensure the table has clear headers and rows are properly aligned.
    
    Content Styling:
    Use consistent font styles and sizes throughout the response.
    Separate paragraphs with appropriate spacing for readability.
    Utilize bullet points or numbered lists for better organization if necessary.
    
    Overall Layout:
    Maintain a clean and organized layout for the entire response.
    Align container on left
    
    Provide response with HTML and Bootstrap
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
    )
    
    # print(response)
    
    # Ensure response is not empty and contains choices
    if response and response.choices:
        # Extract JSON content from the first choice
        json_content = response.choices[0].message.content
        # Attempt to load JSON content
        try:
            return json_content
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("No response or choices found.")