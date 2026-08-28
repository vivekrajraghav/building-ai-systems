import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel

#Getting Variable from .env
load_dotenv()

# loading Groq API Key
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Missing")

# Creating Client and selecting model
client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

# Structuring Output of LLM using Pydantic Library
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    customer_id:int

# Creating Schema 
schema=Ticket.model_json_schema()

# passing resonse type
response_format={
    "type":"json_object"
}

# System prompt for getting desired output in defined schema
system_prompt=f"""
Extract peronal information from tickey strictly based on this schema and give a json output. {schema}
"""
message_system={
    "role":"system",
    "content":system_prompt
}
# User input text and adding it into prompt
input_text="Hello, Im Vivek, Yesterday I bought a iPhone which is not a working at all now. My address is Delhi. My email is abc@gmail.com.Contact no. 1234567890"
prompt=f"""
This is customer ticket. Please extract personal information from this.Keep the infomation to the point, under issue only 1 word issue category{input_text}
"""
role="user"
message={
    "role":"user",
    "content":prompt
}

# Creating Array of messages
messages=[message_system,message]

# Getting response from LLM
respone=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer=respone.choices[0].message.content
print(answer)

# Reading Raw JSON file
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

# Printing details from JSON
print(ticket.name)
print(ticket.email)
print(ticket.issue)
print(ticket.customer_id)