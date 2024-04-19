from openai import OpenAI
import json

def get_classification_intent(query):
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful assistant, please classify user query into two categories: quantitative user queries or subjective user queries. If any particular question type, such as listing of any data, is present in the user query excluding those starting with 'What', it should be considered as a quantitative query. And also provide the classification intent with confidence score and user query in a JSON format. Generate a JSON object with the following structure: '{\"query\":\"value\", \"intent\":\"value\", \"relevance_score\":\"value\"}'"},
            {"role": "user", "content": query},
        ]
    )
    # Ensure response is not empty and contains choices
    if response and response.choices:
        # Extract JSON content from the first choice
        json_content = response.choices[0].message.content
        
        # Attempt to load JSON content
        try:
            json_data = json.loads(json_content)
            intent = json_data.get('intent')
            return intent
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("No response or choices found.")


# get_classification_intent("What are the different CRM tools In Time Tec has experience working with?")