import os
from dotenv import load_dotenv
import json
import anthropic
import openai
from tqdm import notebook
import numpy as np
from together import Together
import random
import streamlit as st
from prompts import princess_lily_system, hero_volt_system, dog_buddy_system

# Try to load environment variables from .env file if it exists
try:
    load_dotenv()
except Exception:
    pass  # Proceed without .env file (for deployment)

# Try to get API key from Streamlit secrets first, then fall back to environment variables
try:
    together_api_key = st.secrets["together"]["api_key"]
except Exception:
    together_api_key = os.getenv('TOGETHER_API_KEY', '')

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY', '')
openai_api_key = os.getenv('OPENAI_API_KEY', '')

# Validate required API key
if not together_api_key:
    raise ValueError("TOGETHER_API_KEY is required but not found in Streamlit secrets or environment variables")

def data_gen(inputs, difficulty_level=0, model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
    # Initialize Together client with the correct API
    Together.api_key = together_api_key
    together_client = Together()

    # Select system prompt based on difficulty level
    system_prompts = {
        0: princess_lily_system["easy"],
        1: princess_lily_system["medium"],
        2: princess_lily_system["hard"]
    }
    system = system_prompts.get(difficulty_level, princess_lily_system["easy"])

    success = False
    while not success:
        try: 
            response = together_client.chat.completions.create(
                model=model_name,
                messages=[
                    {   
                        "role": "system",
                        "content": system
                    },
                    {
                        "role": "user",
                        "content": inputs
                    }
                ],
                max_tokens=1000,
                temperature=1,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>","<|eom_id|>"],
                stream=True
            )
            outputs = []
            for token in response:
                if hasattr(token, 'choices'):
                    outputs+=token.choices[0].delta.content                    
            outputs = ''.join(outputs)
            success = True
        except Exception as e:
            print(f"Error during generation or extraction: {e}")
            # If there's an error, return a friendly message
            return "I apologize, but I'm having trouble processing your request at the moment. Please try again."
    return outputs
