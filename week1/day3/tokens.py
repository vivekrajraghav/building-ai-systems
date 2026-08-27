import os
from dotenv import load_dotenv
from groq import Groq

# Loading the variable from .env file
load_dotenv()

# Getting API Key from .env file
my_api_key=os.getenv("GROQ_API_KEY")

# Error for missing API
if not my_api_key:
    raise ValueError("API Key is missing")

# Creating GROQ Client
client=Groq(api_key=my_api_key)

#Selecting model
model="openai/gpt-oss-120b"

# Creating Prompt and role
role="user"
prompt1="Hi!"
prompt2="Brief history of IIT Roorkee"
prompt3="Describe the Diwali festival in details"
prompts=[prompt1,prompt2,prompt3]

# Passing response to LLM through Iteration
for prompt in prompts:
    message={
        "role":role,
        "content":prompt
    }
    messages=[message]
    response=client.chat.completions.create(model=model,messages=messages,max_tokens=500)
    usage=response.usage
    print(f"Prompt: {prompt} --> your token {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} total_tokens: {usage.total_tokens} finish_reason: {response.choices[0].finish_reason}")
    print(response.choices[0].message.content)
    print("-"*30)