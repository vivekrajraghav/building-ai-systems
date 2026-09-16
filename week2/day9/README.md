# 🚀 Week 2, Day 9: Real-Time LLM Streaming

![Python](https://img.shields.io/badge/Python-3.11-blue.svg?logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F37B60)
![Streaming](https://img.shields.io/badge/Streaming-SSE-059142) 

This document demonstrates how to implement **Server-Sent Events (SSE) streaming** using the Groq API. Instead of waiting for an entire Large Language Model response to generate before displaying it, this script streams the output token-by-token in real-time, drastically reducing the Time-to-First-Token (TTFT) and improving User Experience (UX).

---

## ✨ Core Concepts

### 1. Time-to-First-Token (TTFT)
In AI engineering, TTFT is a critical metric. It measures the milliseconds between a user hitting "enter" and the first word appearing on the screen. Streaming optimizes TTFT by returning partial data chunks immediately while the model is still processing the rest of the answer.

### 2. Delta vs. Message
In a standard API call, the response payload is located at `choices[0].message.content`. When streaming, the data arrives in tiny fragments called "deltas." We extract these fragments dynamically using `choices[0].delta.content`.

### 3. Buffer Flushing
Standard Python `print()` statements hold text in a hidden buffer until an entire line is complete. To create a typewriter effect, we must bypass this buffer by forcefully flushing the output directly to the terminal as soon as a token arrives.

---

## 🛠️ The Code (`stream_response.py`)

```python
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API Key
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key is not available")

# Initialize Client
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

prompt = "Explain rules of cricket in 500 words"
message = {
    "role": "user",
    "content": prompt
}
messages = [message]

# 1. Enable Streaming mode in the API call
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)

# 2. Iterate through the incoming data chunks
for chunk in stream:
    # 3. Extract the delta content instead of the full message
    content = chunk.choices[0].delta.content
    
    if content:
        # 4. Print without a newline and force flush the buffer
        print(content, end="", flush=True)

```

---

## 🧠 Code Breakdown

* `stream=True`: This single boolean flag changes the Groq API's behavior from a standard REST POST request into a persistent, open connection that streams data as it is generated.
* `for chunk in stream:`: Because `stream` is an iterable generator, the script enters a loop, waiting for the Groq server to push the next piece of text over the network.
* `end=""`: Prevents Python from automatically moving to a new line after every single word.
* `flush=True`: Forces Python's standard output stream to display the text immediately on the screen, creating the classic "AI typing" visual effect.

---

## 🔄 System Architecture: Standard vs. Streaming

```mermaid
graph TD
    subgraph Standard API Call (High Latency)
    A[Send Prompt] -->|Wait 5s| B[LLM Generates 100% of Text]
    B --> C[Return Full Payload]
    C --> D[Print Block of Text]
    end
    
    subgraph Streaming API Call (Low Latency)
    E[Send Prompt] -->|Wait 0.2s| F[LLM Generates 1st Token]
    F --> G[Return Chunk 1]
    G --> H[Print Token]
    
    F -->|Wait 0.1s| I[LLM Generates 2nd Token]
    I --> J[Return Chunk 2]
    J --> K[Print Token]
    
    H -.->|Real-time Loop| K
    end
    
    style Standard API Call fill:#ffebee,stroke:#f44336,stroke-width:2px
    style Streaming API Call fill:#e8f5e9,stroke:#4caf50,stroke-width:2px

```