from ollama import chat
import gradio as gr
from datetime import datetime
import tts
from datetime import datetime
import json
from json import JSONDecodeError
    
def time_taken(instruction, chunks, LLM_end_time, LLM_start_time):
    with open("outputs/time_taken/time_taken.txt", "a") as f:
        f.write(f"instruction:\n{instruction}\nAI:\n{chunks}\n" + f"Time taken by LLM: {LLM_end_time - LLM_start_time}\n\n--------------------------------------------------\n\n")
    
def get_chat_history():
    with open('chat_history.txt', 'r') as f:
        chat_history = f.read()
        #json_chat_history = json.loads(chat_history)
    return chat_history
        
def save_current_conversation(current_conversation):
    with open('chat_history_database.txt', 'a') as f:
        f.write(current_conversation)
        
def save_current_booking(current_booking):
    with open('chat_history.txt', 'w') as f:
        f.write(current_booking)
        
def generate(user, current_conversation):
    instruction = """You are a cab booking assistant.
    You will be provided with a user question. Your task is to get the required details to book a cab and once you got all the required details, then respond with the below json structure. 
    **Required details:**
    a) Pickup and Drop locations
    b) Date and Time
    c) Number of passengers
    d) Type of cab
    If asking details, ask them one by one in short.
    Before asking questions, read through the chat_history carefully and see if the details related to the current booking are already given.
    If all the details are already given, you can respond with the below json structure. If not, you need to ask the required details.
    Remember while asking questions, ask one question at a time and wait for the user to respond before asking the next question.
    Your response must NOT contain any special characters or punctuations or numbers."""
    
    test_instruction = """You are a fill in the json structure expert.
You will be provided with a JSON structure. Your task is to:

Extract the required values from the user_input to populate the fields in the JSON structure.
If any values cannot be extracted from the user_input, populate the assistant key of the JSON structure with questions asking the missing details.
Ensure the JSON structure is completed accurately, either by directly filling the extracted values or by adding relevant queries in the assistant key.
Don't respond with any words, special characters, punctuations, or numbers except the json structure.
Just do what you are told to do. Don't add any extra information or ask any questions.

Examples:
user: 'I want to book a cab from Alpha hospital to Konar mess'
assitant: {"pickup_location" : "Alpha hospital", "drop_location" : "Konar mess", "pickup_time" : "None", "cab_type" : "None", "user_input" : "Ahh near konar mess", "assistant" : ["What is your preferred pickup time?", "Which cab type would you like (e.g. auto, sedan etc)?"]}

user: 'at 10 pm'
assistant: {"pickup_location" : "Alpha hospital", "drop_location" : "Konar mess", "pickup_time" : "5pm", "cab_type" : "None", "user_input" : "Ahh near konar mess", "assistant" : ["Which cab type would you like (e.g. auto, sedan etc)?"]}

"""
    #LLM
    LLM_start_time = datetime.now()
    response = chat(
        model = "llama3.2:3b",
        messages = [{'role' : 'assistant', 'content' : test_instruction}, {'role' : 'user', 'content' : user}],
        keep_alive = '10m'
    )
    AI = response['message']['content']
    json_response = json.loads(AI)
    print(json_response)
    
    #Document timetaken for LLM
    LLM_end_time = datetime.now()
    print("Time taken by LLM: ", LLM_end_time - LLM_start_time)
    time_taken(instruction, response, LLM_end_time, LLM_start_time)
    
    #Document chat history
    current_conversation += "User: " + user + "\n\n" + "assistant: " + AI + "\n\n\n"
    save_current_conversation(current_conversation)
    save_current_booking(AI)
    

def main(user):
    chat_history = get_chat_history()
    current_conversation = ""
    generate(user, current_conversation)
    
if __name__ == "__main__":
    text = """{"pickup_location" : "Teppakulam", "drop_location" : "Anannagar", "pickup_time" : "None", "cab_type" : "None", "user_input" : "5 pm bro", "assistant" : []} """
    main(text)

