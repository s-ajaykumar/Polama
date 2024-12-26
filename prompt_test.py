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


with open('databases/chat_history.txt', 'r') as f:
    content = f.read()
previous_json = json.loads(content)
del previous_json["user_input"]
#Fill the "None" values with details from the user query (or) from asking a question. 

LLM_instruction = f"""You are a cab booking assitant. 
You will be provided with a JSON structure and a user query. Read through them carefully. Your task is to:

Still if there are "None" values to be filled in the JSON structure, fill them using the user query if details are present in it and if details are not present in the user query, ask the details to be filled. 
Else, if all the details are present in the user query, give a thankyou and end the conversation.
If asking cab type, list the cab_types: auto, innova, swift desire and ask to choose.

Do NOT ask for already provided details.
If a detail is provided, do NOT ask for specificity of it and just keep it as it is.
Do NOT ask extra questions.
Ask one question at a time and ask it in a single sentence within 10 to 15 words.
Your response must NOT contain any special characters or punctuations or numbers. 

json_structure:
{previous_json}
"""
details = f"pickup_location: {previous_json['pickup_location']}\ndrop_location: {previous_json['drop_location']}\npickup_time: {previous_json['pickup_time']}\nnumber of passengers: {previous_json['number of passengers']}\ncab_type: {previous_json['cab_type']}\n"
i = f"""User provided you with some cab booking details in the previous conversations. Your task is to:
Compare the user provided details and the user query with the required details, check if any required detail is missing or not. 
[required_details: Pickup and Drop locations, PickupTime, Number of passengers, Type of cab]
If any required details are missing in the user provided details then ask them one at a time. Ask it in less than 15 words.
If not a single required detail is missing in the user provided details then don't ask any question, thank the user ending the conversation in less than 15 words.

user provided details:
{details}
"""
print(i,"\n\n")
#Don't repeat a question if the detail is already provided.
text = "3 bro"
with open('databases/AI_response_database.txt', 'r') as f:
    AI = f.read()
start_time = datetime.now()

response = chat(
    model = "llama3.2:3b",
    messages = [{'role' : 'system', 'content' : i}, {"role" : "assistant", "content" : AI}, {'role' : 'user', 'content' : text}],
    keep_alive = '59m',
    options = {'temperature' : 0}
)

print(response['message']['content'], "\n")
with open('databases/AI_response_database.txt', 'w') as f:
    f.write(response['message']['content'])
end_time = datetime.now()
print("Time taken by chatLLM: ", end_time - start_time)