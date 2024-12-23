from ollama import chat
from ollama import ChatResponse
import gradio as gr
from datetime import datetime
import tts
from datetime import datetime
import subprocess
import json
import config

def search_places(pickup_location: str = None, drop_location: str = None):
    if drop_location is None:
        print("Getting pickup location only...")
        text = f"""{{
        "address": {{
            "regionCode": "IN",
            "addressLines": ["{pickup_location}"]
        }}
    }}"""
        curl_command = [
            "curl",
            "-X", "POST", "https://addressvalidation.googleapis.com/v1:validateAddress?key="+config.google_api_key,
            "-H", "Content-Type: application/json",
            "-d", text
        ]
        
        try:
            response = subprocess.run(curl_command, capture_output = True, text = True)
            json_response = json.loads(response.stdout)
            print(json_response)
        except Exception as e:
            print(response.stderr)
            print(e)
            
    if pickup_location is None:
        print("Getting drop location only...")
        text = f"""{{
        "address": {{
            "regionCode": "IN",
            "addressLines": ["{drop_location}"]
        }}
    }}"""
        curl_command = [
            "curl",
            "-X", "POST", "https://addressvalidation.googleapis.com/v1:validateAddress?key="+config.google_api_key,
            "-H", "Content-Type: application/json",
            "-d", text
        ]
        
        try:
            response = subprocess.run(curl_command, capture_output = True, text = True)
            json_response = json.loads(response.stdout)
            print(json_response)
        except Exception as e:
            print(response.stderr)
            print(e) 
        
    else:
        print("Getting both pickup and drop locations...")
        text1 = f"""{{
        "address": {{
            "regionCode": "IN",
            "addressLines": ["{pickup_location}"]
        }}
    }}"""
        text2 = f"""{{
            "address": {{
                "regionCode": "IN",
                "addressLines": ["{drop_location}"]
                }}
            }}"""
        curl_command1 = [
            "curl",
            "-X", "POST", "https://addressvalidation.googleapis.com/v1:validateAddress?key="+config.google_api_key,
            "-H", "Content-Type: application/json",
            "-d", text1
        ]
        curl_command2 = [
            "curl",
            "-X", "POST", "https://addressvalidation.googleapis.com/v1:validateAddress?key="+config.google_api_key,
            "-H", "Content-Type: application/json",
            "-d", text2
        ]
        try:
            response1 = subprocess.run(curl_command1, capture_output = True, text = True)
            response2 = subprocess.run(curl_command2, capture_output = True, text = True)
            json_response1 = json.loads(response1.stdout)
            json_response2 = json.loads(response2.stdout)
            print(json_response1,"\n\n", json_response2)
            if json_response1['result']['verdict']['inputGranularity'] == 'PREMISE' and json_response2['result']['verdict']['validationGranularity'] == 'PREMISE' and json_response1['result']['verdict']['geocodeGranularity'] == 'PREMISE':
                geocodes = json_response1['result']['geocode']['location']
                print("Both locations are valid\n\n")
                print("Geocodes: ", geocodes)
            if json_response1['result']['verdict']['inputGranularity'] == 'OTHER' or json_response1['result']['verdict']['validationGranularity'] == 'OTHER':
                print(f"Can you tell me more specifically in {pickup_location}? or any landmarks nearby?\n\n")
            if json_response2['result']['verdict']['inputGranularity'] == 'OTHER' or json_response2['result']['verdict']['validationGranularity'] == 'OTHER':
                return print(f"Can you tell me more specifically in the {drop_location}? or any landmarks nearby?\n\n")
        except Exception as e:
            print(response1.stderr, response2.stderr)
            print(e)
    
    
def generate(user):
    instruction = """Your task is to verify the pickup and drop locations. Use the available tools to verify the locations."""
    
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
    main("bro near alpha hospital madurai want to go to simmakkal how much bro")
