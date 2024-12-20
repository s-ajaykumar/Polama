from ollama import chat
import gradio as gr
from datetime import datetime
import tts
from datetime import datetime
    
    
def time_taken(instruction, chunks, LLM_end_time, LLM_start_time):
    with open("outputs/time_taken/time_taken.txt", "a") as f:
        f.write(f"instruction:\n{instruction}\nAI:\n{chunks}\n" + f"Time taken by LLM: {LLM_end_time - LLM_start_time}\n\n--------------------------------------------------\n\n")
    
def get_chat_history():
    with open('chat_history.txt', 'r') as f:
        chat_history = f.read()
    return chat_history
        
def save_current_conversation(current_conversation):
    with open('chat_history.txt', 'a') as f:
        f.write(current_conversation)
    with open('chat_history_database.txt', 'a') as f:
        f.write(current_conversation)
        
def generate(user, current_conversation, chat_history):
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
    
    current_conversation += "User: " + user + "\n\n"
    
    #LLM
    LLM_start_time = datetime.now()
    response = chat(
        model = "llama3.2:1b",
        messages = [{'role' : 'assistant', 'content' : instruction}, {'role' : 'user', 'content' : user}],
        stream = True
    )

    chunks = ""
    for chunk in response:
        print(chunk['message']['content'], end = "", flush = True)
        chunks += chunk['message']['content']
    
    #Document timetaken for LLM
    LLM_end_time = datetime.now()
    print("Time taken by LLM: ", LLM_end_time - LLM_start_time)
    time_taken(instruction, chunks, LLM_end_time, LLM_start_time)
    #Document chat history
    current_conversation += "assistant: " + chunks + "\n\n\n"
    save_current_conversation(current_conversation)
    
    


def main(user):
    chat_history = get_chat_history()
    current_conversation = ""
    generate(user, current_conversation, chat_history)
    
if __name__ == "__main__":
    main("want to go from kalavasal to simmakkal")

