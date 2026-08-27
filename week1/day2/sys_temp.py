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
prompt="I forgot to submit the assignment also I was not present on the assignment was given"

# System Message
system_message={
    "role":"system",
    "content":"You are strict teacher who is famous for punishing students for misbehave"
}
# Defining the role and passing the prompt
message={
            "role":role,
            "content":prompt
        }
messages=[system_message,message]
# Sending request to LLM (Groq)
# Temperature by deafault 0 meaning safe. It ranges from [0,2] where 0 for safe and 2 for highest creative reponses
response=client.chat.completions.create(model=model, messages=messages,temperature=2)

# Choosing first generated reponse
answer=response.choices[0].message.content
print(answer)

