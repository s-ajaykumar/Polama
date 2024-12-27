from ollama import chat
from datetime import datetime
import json

with open('chat_database_test.txt', 'r') as f:
    chat_history = f.read()

instruction = f"""<instructions>
You are a cab booking assistant. 
Your task is to get the required details to book a cab.
<required_details>
pickup_location, drop_location, pickup_time, number of passengers, cab_type
<required_details>

Follow the below guidelines to get the details:
- Read through the below conversations and ask the <required_details> missing in the conversations.
- Ask one detail at a time in less than 10 words.

Follow the below guidelines while responding to the user:
- Never ask the <required_details> provided by the user in the below conversations again.
- If and only if all the <required_details> are provided by the user in the below conversations, say "Thank you" and end the conversation.
</instructions>

{chat_history}
"""
print(instruction, "\n")

user = "3"
start_time = datetime.now()
response = chat(
    model = "gemma2:2b",
    messages = [{'role' : 'system', 'content' : instruction}, {"role": "user", "content": user}],
    keep_alive = -1,
    options = {"temperature": 0}
)
conversation = f"user: {user}\nassistant: {response['message']['content']}\n\n"
with open('chat_database_test.txt', 'a') as f:
    f.write(conversation)
print(conversation)
end_time = datetime.now()
print("Time taken: ", end_time - start_time)