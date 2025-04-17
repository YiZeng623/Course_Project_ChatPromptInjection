import os
from dotenv import load_dotenv
import numpy as np
from together import Together
from .prompts import princess_lily_system_0, princess_lily_system_1, princess_lily_system_2

# Load environment variables from the .env file
load_dotenv()

# Access the API keys
together_api_key = os.getenv('TOGETHER_API_KEY')

# Define the system prompts for each difficulty level
SYSTEM_PROMPTS = {
    0: princess_lily_system_0,  # Easy
    1: princess_lily_system_1,  # Medium
    2: princess_lily_system_2   # Hard
}

def data_gen(inputs, model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
    together_client = Together(api_key = together_api_key)
    
    # Get the current difficulty level from streamlit session state
    import streamlit as st
    difficulty_level = getattr(st.session_state, 'difficulty_level', 0)
    system = SYSTEM_PROMPTS.get(difficulty_level, princess_lily_system_0)

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


