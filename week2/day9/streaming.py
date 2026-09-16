import os
from groq import Groq
from dotenv import load_dotenv
from time import sleep

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key is not available")
client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

prompt="Explain rules of cricket in 500 words"
message={
    "role":"user",
    "content":prompt
}
messages=[message]
stream=client.chat.completions.create(model=model,messages=messages,stream=True)
for chunk in stream:
    content=chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)