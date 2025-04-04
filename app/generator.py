import os
from dotenv import load_dotenv
import json
import anthropic
import openai
from tqdm import notebook
import numpy as np
from together import Together
import random
from prompts import princess_lily_system, hero_volt_system, dog_buddy_system

# Load environment variables from the .env file
load_dotenv()

# Access the API keys
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
together_api_key = os.getenv('TOGETHER_API_KEY')

def data_gen(inputs, difficulty_level=0, model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
# def data_gen(inputs, system=hero_volt_system, model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
# def data_gen(inputs, system=dog_buddy_system, model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
    together_client = Together(api_key = together_api_key)

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
    return outputs
