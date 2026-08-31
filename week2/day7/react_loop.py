import os
import re
from time import sleep
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Groq client
my_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"


def get_product_price(product):
    if product == "iPhone 17":
        return 150000
    elif product == "iPhone 15":
        return 80000
    else:
        return 0
def calculator(expression):
    try:
        return eval(expression)
    except:
        return "Cal error"
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}
system_prompt = """
You are a shopping assistant.
You have these tools:
calculator(expression)
get_product_price(product)

Important:
Call tools exactly like this:
Action: get_product_price("iPhone 17")
Action: calculator("56266-32632")

Never write:
get_product_price(product="iPhone 17")
calculator(expression="7555-6662")

Follow these rules:
1. Decide what you need to do next
2. Call only One tool at a time
3. After writing an Action, stop immediately
4. Wait until receive an observation
5. Then decide your next action
6. When task is complete, give Final Answer 

Format:
Thought: What you need to do
Action: tool_name(argument)

Final Answer: your answer
"""

def run_agent(question,tools=tools):
    # Initialize conversation history
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for step in range(5):
        print("\n--------------------------")
        print(f"STEP: {step+1}")
        print("--------------------------")
        
        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        answer = response.choices[0].message.content
        print(answer)

        # Stop if the agent solved it
        if "Final Answer" in answer:
            break
            
        # Parse the Action and arguments out of the LLM's response
        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer
        )
        
        if match:
            tool_name = match.group(1)
            tool_input = match.group(2)
            
            # Clean up rogue spaces or quotes the LLM might add
            tool_input = tool_input.strip().strip('"')

            # Execute the tool if it exists in our dictionary
            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)
            else:
                observation = "Tool not found"
                
            print("Observation:", observation)

            # Update memory so the LLM remembers what it just did...
            messages.append({
                "role": "assistant",
                "content": answer
            })

            # ...and feed the result back for the next iteration
            messages.append({
                "role": "user",
                "content": "Observation: " + str(observation)
            })
            
            sleep(5)

prompt = """
I have 200000 rupees. what is price of an iPhone 15 and?
and how much money  will I have left?
"""

run_agent(prompt)