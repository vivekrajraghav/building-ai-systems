import os
from dotenv import load_dotenv
from groq import Groq

#Loading variables from .env file
load_dotenv()

# Get API key from .env File for GROQ
my_api_key=os.getenv("GROQ_API_KEY")

# Error Message if API not found
if not my_api_key:
    raise ValueError("GROQ_API_KEY is missing")

# Creating Groq client
client=Groq(api_key=my_api_key)

# Selecting model
model = "openai/gpt-oss-120b"

# Creating prompt and Role
role="user"
prompt="Give a short summary on types of machine learning"

# Defining the role and passing the prompt
message=[
        {
            "role":role,
            "content":prompt
        }]

# Sending request to LLM (Groq)
response=client.chat.completions.create(model=model, messages=message)

# Getting answers: Multiple generated choices
print(response)

# # Choosing first generated reponse
print("-"*20)
answer=response.choices[0].message.content
print(answer)

