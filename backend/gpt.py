import re
import json
from g4f.client import Client
import openai
from typing import Tuple, List  
from termcolor import colored
import os
import google.generativeai as genai

# Load environment variables

# Set environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


def generate_response(prompt: str, ai_model: str) -> str:
    """
    Generate a script for a video, depending on the subject of the video.

    Args:
        prompt (str): The subject of the video.
        ai_model (str): The AI model to use for generation.

    Returns:
        str: The response from the AI model.

    """

    if ai_model in ["gpt3.5-turbo", "gpt4"]:

        model_name = "gpt-3.5-turbo" if ai_model == "gpt3.5-turbo" else "gpt-4-1106-preview"
        client = Client()

        response = client.chat.completions.create(

            model=model_name,

            messages=[{"role": "user", "content": prompt}],

        ).choices[0].message.content
    elif ai_model == 'gemmini':
        model = genai.GenerativeModel('gemini-pro')
        response_model = model.generate_content(prompt)
        response = response_model.text

    else:

        raise ValueError("Invalid AI model selected.")

    return response

def generate_5w1h_summary(article_json: str, ai_model: str) -> str:

    """
    Generate 5w and 1h based summary of articles list given.
    Args:

        article_json (str): The json containing list of multiple articles.

        ai_model (str): The AI model to use for generation.

    Returns:

        str: The 5w and 1h summary of the article list

    """

    prompt = """Write the name of the event, type of the event,
                involved person, involved countries and the location of the
                event from the following news. Use IPTC media topic name
                while writing values for 'Event type'. Write full name while
                mentioning involved persons and locations. Write only name
                of persons if they are known. No need to include any
                unknown person. Also do not need to write the designation
                or position of the persons. While returning the location,
                mention the country where the event took place. While
                returning the iptc media topic names, please return the
                output for which you are significantly confident about.
                If there are more values, generate an array json.
                List 5W and 1H questions surrouding the topic referencing the articles.
                Also list the important search keywords which can help us gain more information about the issue.
                The answer to those questions. 
                Format your answer as a JSON object
                with the following key-values:
                {
                    “Event": “event-name",
                    “Event Type": “iptc-media-topic-name",
                    “Involved Countries": “country-name",
                    “Location of Event": “city-name",
                    “Involved-People": {1:“Person1-name", 2:“Person2-name",3:“Person3-name", ....},
                    "what": {"question": "what-question", "answer": "what-answer"}, 
                    "who": {"question": "who-question", "answer": "who-answer"}, 
                    "where": {"question": "where-question", "answer": "where-answer"}, 
                    "why": {"question": "why-question", "answer": "why-answer"}, 
                    "when": {"question": "when-question", "answer": "when-answer"},
                    "how": {"question": "how-question", "answer": "how-answer"},
                    "search_keywords": {1:"search-keyword1,2:"search-keyword2,3:"search-keyword3, ....}
                }
                the news:""" + article_json
    response = generate_response(prompt, ai_model)

    if response:
        # Clean the script
        # Remove asterisks, hashes
        response = response.replace("*", "")
        response = response.replace("#", "")

        # Remove markdown syntax
        response = re.sub(r"\[.*\]", "", response)
        response = re.sub(r"\(.*\)", "", response)

        return response
    else:
        print(colored("[-] GPT returned an empty response.", "red"))
        return None
