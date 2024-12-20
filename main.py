from ollama import chat
import gradio as gr
from datetime import datetime
import tts

    
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
    You will be provided with a user question. Your task is to Ask the required details to book a cab and book for him/her. 
    Before asking questions, read through the chat_history carefully and see if the details related to the current booking are already given.
    If the details are already given, you can directly book the cab. If not, you need to ask the required details.
    Remember while asking questions, ask one question at a time and wait for the user to respond before asking the next question.
    Your response must NOT contain any special characters or punctuations or numbers."""
    

    current_conversation += "User: " + user + "\n\n"

    response = chat(
        model = "llama3.2:3b",
        messages = [{'role' : 'assistant', 'content' : instruction}, {'role' : 'user', 'content' : f"chat_history:\n{chat_history}\n\n" + user}],
        stream = True
    )

    chunks = ""
    for chunk in response:
        print(chunk['message']['content'], end = "", flush = True)
        chunks += chunk['message']['content']

    #Update chat history
    current_conversation += "assistant: " + chunks + "\n\n\n"
    save_current_conversation(current_conversation)
    
    return chunks


def main(user):
    chat_history = get_chat_history()
    current_conversation = ""
    #user = "want to go from kalavasal to simmakal"
    AI = generate(user, current_conversation, chat_history)
    mp3_path = tts.tts(AI)
    return mp3_path
'''if __name__ == "__main__":
    main()'''


#gradio interface
app = gr.Interface(
    fn = main,
    inputs = [gr.Text(label = 'Shall I book a cab for you :)')],
    outputs = [gr.Audio(label="AI")]
)
app.launch()