from ollama import chat
from ollama import ChatResponse
import gradio as gr
from datetime import datetime
import tts
from datetime import datetime
import subprocess
import json

def search_places(pickup_location: str, drop_location: str):
    text1 = f'{{"textQuery" : "{pickup_location}"}}'
    text2 = f'{{"textQuery" : "{drop_location}"}}'
    curl_command1 = [
        "curl",
        "-X", "POST", "https://places.googleapis.com/v1/places:searchText",
        "-H", "Content-Type: application/json",
        "-H", 'X-Goog-Api-Key: AIzaSyBleud1_wi7WpsveLreqq-sDSOL2nJKDPQ',
        "-H", 'X-Goog-FieldMask: places.displayName,places.formattedAddress,places.priceLevel',
        "-d", text1
    ]
    curl_command2 = [
        "curl",
        "-X", "POST", "https://places.googleapis.com/v1/places:searchText",
        "-H", "Content-Type: application/json",
        "-H", 'X-Goog-Api-Key: AIzaSyBleud1_wi7WpsveLreqq-sDSOL2nJKDPQ',
        "-H", 'X-Goog-FieldMask: places.displayName,places.formattedAddress,places.priceLevel',
        "-d", text2
    ]
    try:
        response1 = subprocess.run(curl_command1, capture_output = True, text = True)
        response2 = subprocess.run(curl_command2, capture_output = True, text = True)
        json_response1 = json.loads(response1.stdout)
        json_response2 = json.loads(response2.stdout)
        final_out = f"pickup_location: {json_response1['places'][0]['formattedAddress']}\ndrop_location: {json_response2['places'][0]['formattedAddress']}" 
        return final_out
    except Exception as e:
        print(response1.stderr, response2.stderr)
        print(e)    
        return e
    
    
def generate(user):
    instruction = """You are a cab booking assistant.
    You will be provided with a user question. Your task is to get and verify the pickup and drop locations. Use the available tools to verify the locations."""
    
    
    
    #LLM
    LLM_start_time = datetime.now()
    response: ChatResponse = chat(
        model = "llama3.2:3b",
        messages = [{'role' : 'assistant', 'content' : instruction}, {'role' : 'user', 'content' : user}],
        tools = [search_places]
    )
    
    #Document timetaken for LLM
    LLM_end_time = datetime.now()
    print("Time taken by LLM: ", LLM_end_time - LLM_start_time, "\n\n")
    
    available_functions = {
    'search_places': search_places
    }
    
    if response.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_functions.get(tool.function.name):
                print('Calling function:', tool.function.name)
                print('Arguments:', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                print('Function output:', output)
            else:
                print('Function', tool.function.name, 'not found')

    else:
        print('No tool calls returned from model')


def main(user):
    generate(user)
    
    
if __name__ == "__main__":
    main("want to go from kalavasal to simmakkal")
