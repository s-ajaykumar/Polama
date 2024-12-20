import subprocess
from datetime import datetime


def tts(text):

    # Correct way to include the text variable inside the f-string
    input = f'{{"text": "{text}"}}'
    formatted_input = input.replace("\n\n", "n")
    
    curl_command = [
        "curl",
        "-X", "POST", "https://api.elevenlabs.io/v1/text-to-speech/9BWtsMINqrJLrRacOk9x",
        "-H", "xi-api-key: sk_1e40f33a8721737efa7459986537820cb28a8605bf1fc23d",  # Replace <apiKey> with your actual API key
        "-H", "Content-Type: application/json",
        "-d", formatted_input  # Replace <text> with the text you want to convert to speech
    ]
    try:
        print("tts started..")
        result = subprocess.run(curl_command, capture_output=True)
        print("tts finished successfully")

    except Exception as e:
        print(e)
        
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H:%M")
    file_path = "outputs/" + current_datetime + ".mp3"
    with open(file_path, "wb") as f:
        f.write(result.stdout)
        print("mp3 saved")
    
    return file_path
