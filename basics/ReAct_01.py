import os
from pathlib import Path
from time import sleep
from groq import Groq
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
model="qwen/qwen3.8-27b" 

client = Groq(api_key=GROQ_API_KEY)

# sample tool
def calculate(expression):
    try:
        return eval(expression)
    except:
        return "error calculating"
def get_product_price(product):
    if product=='laptop':
        return 120000
    elif product=='mobile':
        return 80000
    else:
        return 0

tools={
    "get_product_price":get_product_price,
    "calculate":calculate,
}


system_prompt = """
# ROLE
You are an AI shopping assistant.

# AVAILABLE TOOLS
1. get_product_price(product)
2. calculate(expression)

# EXAMPLE
Thought: I need the mobile price first.
Action: get_product_price("mobile")

# STRICT RULES

1. You MUST use tools to obtain factual product prices.
2. Never assume or invent tool results.
3. You MUST call only one tool per response.
4. After calling a tool, WAIT for its observation.
5. Use the observation to decide your next action.
6. Never use placeholders like [price] or [remaining amount].
7. Never calculate using information you have not received.
8. Never provide a final answer until all required tools
   have been executed and their observations received.
9. If the task requires multiple tools, execute them sequentially.

# RESPONSE FORMAT

When a tool is required:

Thought: Explain what you need.
Action: tool_name("argument")

When the task is completed using the tools:

Final Answer: Give the actual answer using tool observations.

# IMPORTANT
For this particular task:
- First get the mobile price.
- Then calculate the remaining budget.
- Finally provide the answer.

Do not skip any step.
"""


def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):

        print("------------------------")
        print(f"STEP {step + 1}")
        print("------------------------\n")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            stop=["Observation:"],
        )

        answer = response.choices[0].message.content or ""

        print("LLM: ", answer)

        # 1. Check whether the agent has completed the task
        if re.search(r"final answer\s*:", answer, re.IGNORECASE):
            print("\nAgent completed successfully!")
            return answer
        
        

        # 2. Extract action
        match = re.search(
                r'Action:\s*(\w+)\s*\((.*?)\)',
                answer,
                re.IGNORECASE | re.DOTALL
            )

        # 3. Handle invalid action
        if match:
        # 4. Extract tool name and argument
            tool_name = match.group(1)
            tool_input = match.group(2).strip().strip('"').strip("'")

            print("\nTOOL:", tool_name)
            print("INPUT:", tool_input)

            # 5. Execute tool
            if tool_name in tools:

                try:
                    tool = tools[tool_name]
                    observation = tool(tool_input)

                except Exception as e:
                    observation = f"Tool execution error: {e}"

            else:
                observation = f"Tool '{tool_name}' not found."

            print("\nOBSERVATION:", observation)

            # 6. Save LLM response
            messages.append({
                "role": "assistant",
                "content": answer
            })

            # 7. Send observation back to LLM
            messages.append({
                "role": "user",
                "content": f"""
                Observation from tool '{tool_name}':
                {observation}

                Based on this observation, decide your next action.
                If the task is complete, provide Final Answer.
                """
            })

        elif re.search(r"final answer\s*:", answer, re.IGNORECASE):
            return answer
        if not match:
            print("No valid action found.")
            messages.append({
                "role": "assistant",
                "content": answer
            })
            messages.append({
                "role": "user",
                "content": "Your response must contain one valid Action or a Final Answer. Continue."
            })
            continue



    print("\nMaximum steps reached.")
    return None


prompt="""

I have 200000 taka to buy a smart device for attending meetings , relaxing and doing the entertaintment 
activities . The device should be portable
I would buy a mobile phone .
How much money I would have left after buying the mobile?
"""

run_agent(prompt)
