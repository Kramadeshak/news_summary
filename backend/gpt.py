import re
import json
import g4f
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

    if ai_model == 'g4f':

        response = g4f.ChatCompletion.create(

            model=g4f.models.gpt_35_turbo_16k_0613,

            messages=[{"role": "user", "content": prompt}],

        )

    elif ai_model in ["gpt3.5-turbo", "gpt4"]:

        model_name = "gpt-3.5-turbo" if ai_model == "gpt3.5-turbo" else "gpt-4-1106-preview"

        response = openai.chat.completions.create(

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

    prompt = f"""
            You are being given a json containing a list of titles and articles. These articles are different news articles about a news topic. Process these articles do the following tasks-
            1. Identify the news topic covered by the articles.
            2. List 5W and 1H questions surrouding the topic referencing the articles.
            3. The answer to those questions. 
    Article: {article_json}
        """
    
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
