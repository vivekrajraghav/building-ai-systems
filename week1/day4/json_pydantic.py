import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Missing")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"
role="user"

# Structuring Output
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    customer_id:int

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}
system_prompt=f"""
Extract peronal information from tickey strictly based on this schema and give a json output. {schema}
"""
message_system={
    "role":"system",
    "content":system_prompt
}
input_text="Hello, Im Vivek, Yesterday I bought a iPhone which is not a working at all now. My address is Delhi. My email is abc@gmail.com.Contact no. 1234567890"
prompt=f"""
This is customer ticket. Please extract personal information from this.Keep the infomation to the point, under issue only 1 word issue category{input_text}
"""

message={
    "role":"user",
    "content":prompt
}

messages=[message_system,message]

respone=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer=respone.choices[0].message.content
print(answer)

import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)
print(ticket.customer_id)