from ollama import chat
import gradio as gr
from datetime import datetime
import tts
from datetime import datetime
import json
from json import JSONDecodeError
import multiprocessing
    
    
def get_previous_json():
    with open('databases/chat_history.txt', 'r') as f:
        content = f.read()
    previous_json = json.loads(content)
    return previous_json
        
def save_to_chat_database(conversation):
    with open('databases/chat_history_database.txt', 'a') as f:
        f.write(conversation)
        
def update_json(updated_json):
    with open('databases/chat_history.txt', 'w') as f:
        f.write(updated_json)
    print("Updated JSON successfully.\n")
        
def save_to_summarized_database(input_json, updated_json):
    concatenated_content = f"User:\n{input_json}\nAssistant:\n{updated_json}\n\n\n"
    with open('databases/summarized_database.txt', 'a') as f:
        f.write(concatenated_content)
    print("Saved to summarized database successfully.\n")
        
def summarize(input_json):
    instruction = """You are an expert in filling JSON structure.
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
    
    p2_start_time = datetime.now()
    summarize_response = chat(
        model = "llama3.2:3b",
        messages = [{'role' : 'assistant', 'content' : instruction}, {'role' : 'user', 'content' : f"""{input_json}"""}],
        keep_alive = '59m'
    )
    updated_json = summarize_response['message']['content']
    print("Summarized_content:\n", updated_json, "\n")
    p2_end_time = datetime.now()
    print("Time taken by summarizeLLM: ", p2_end_time - p2_start_time)
    
    #Document chat history and update hte updated json
    save_to_summarized_database(input_json, updated_json)
    update_json(updated_json)
    

def start_summarize_process(text):
    previous_json = get_previous_json()
    previous_json["user_input"] = text
    previous_json["assistant"] = []
    input_json = previous_json
    summarize(input_json)
    
def LLM(text):
    instruction = """You are a cab booking assistant.
You will be provided with a user question. Your task is to get the required details to book a cab for him/her.
**Required details:**
Pickup and Drop locations,
Time,
Number of passengers,
Type of cab.
    
If asking details, ask them one by one, in SHORT.
Your response must NOT contain any special characters or punctuations or numbers."""
    p1_start_time = datetime.now()
    previous_json = get_previous_json()
    input = f"{previous_json}\n\nquestion: {text}"
    LLM_response = chat(
        model = "llama3.2:3b",
        messages = [{'role' : 'assistant', 'content' : instruction}, {'role' : 'user', 'content' : input}],
        keep_alive = '59m'
    )
    print("AI: ", LLM_response['message']['content'], "\n")
    p1_end_time = datetime.now()
    print("Time taken by chatLLM: ", p1_end_time - p1_start_time,"\n\n")
    
    #Document conversation
    conversation = f"user: {input}\nassistant: {LLM_response['message']['content']}\n\n" 
    save_to_chat_database(conversation)
    
if __name__ == "__main__":
    text = "around 11 am bro"
    start_time = datetime.now()
    p1 = multiprocessing.Process(target = LLM, args = (text,))
    p2 = multiprocessing.Process(target = start_summarize_process, args = (text,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end_time = datetime.now()
    print("Total time taken by both processes: ", end_time - start_time)

