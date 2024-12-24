from datetime import datetime
from ollama import chat
import json


summarize_instruction = """You are an expert in filling JSON structure.
You will be provided with a JSON structure. Your task is to:

Extract the required values from the user_input to populate the fields in the JSON structure.
If any values cannot be extracted from the user_input, leave it as "None".
Ensure the JSON structure is completed accurately by directly filling the extracted values.
Also ensure that all the keys and values are enclosed in double quotes.
Don't respond with any words, special characters, punctuations, or numbers except the json structure.

Examples:
user: {"pickup_location" : "None", "drop_location" : "None", "pickup_time" : "None", "cab_type" : "None", "number of passengers" : "None", "user_input" : "I want to book a cab from Alpha hospital to Konar mess"}
assitant: {"pickup_location" : "Alpha hospital", "drop_location" : "Konar mess", "pickup_time" : "None", "cab_type" : "None", "number of passengers" : "None", "user_input" : "I want to book a cab from Alpha hospital to Konar mess"}

user: {"pickup_location" : "muttuparai", "drop_location" : "None", "pickup_time" : "11am", "cab_type" : "auto", "number of passengers" : "5", "user_input" : "aahh theni main bus stand bro"}
assistant: {"pickup_location" : "muttuparai", "drop_location" : "theni main bus stand", "pickup_time" : "11am", "cab_type" : "auto", "number of passengers" : "5", "user_input" : "aahh theni main bus stand bro"}

"""
'''input_json = json.loads("""{"pickup_location" : "simmakkal", "drop_location" : "None", "pickup_time" : "None", "cab_type" : "None", "number of passengers" : "None", "user_input" : "Ahhh to kalavasal bro around 5pm 3 persons may come bro", "assistant" : []}""")  
 
start_time = datetime.now()
summarize_response = chat(
    model = "llama3.2:3b",
    messages = [{'role' : 'assistant', 'content' : instruction}, {'role' : 'user', 'content' : f"""{input_json}"""}],
    keep_alive = '59m'
)
updated_json = summarize_response['message']['content']

print("Summarized_content:\n", updated_json, "\n")
end_time = datetime.now()

print("Time taken by summarizeLLM: ", end_time - start_time)'''

LLM_instruction = """You are a question asker. 
You will be provided with a JSON structure and a user query. Read through them carefully. Your task is to:

Fill the JSON from the query. If any detail is missing, Ask them. Ask one question at a time.

**while_asking_questions**
Ask in a single sentence within 10 to 15 words.
If asking cab type, provide the cab_types: auto, innova, swift desire.
**while_asking_questions**

Your response must NOT contain any special characters or punctuations or numbers. 
"""

#Don't repeat a question if the detail is already provided.
text = "at 10 pm"
with open('databases/AI_response_database.txt', 'r') as f:
    AI = f.read()
with open('databases/chat_history.txt', 'r') as f:
    content = f.read()
previous_json = json.loads(content)
del previous_json["user_input"]
input = f"{previous_json}\nuser_query: {text}"
print(input,"\n\n")

start_time = datetime.now()
response = chat(
    model = "llama3.2:3b",
    messages = [{'role' : 'system', 'content' : LLM_instruction}, {"role" : "assistant", "content" : AI}, {'role' : 'user', 'content' : input}],
    keep_alive = '59m'
)

print(response['message']['content'], "\n")
with open('databases/AI_response_database.txt', 'w') as f:
    f.write(response['message']['content'])
end_time = datetime.now()
print("Time taken by chatLLM: ", end_time - start_time)