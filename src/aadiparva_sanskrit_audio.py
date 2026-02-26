import base64
from dotenv import load_dotenv
from sarvamai import SarvamAI
import os
import json

load_dotenv()

# Retrieve the SARVAM_KEY from environment variables
api_key = os.getenv("SARVAM_KEY")

# Check if the API key is loaded properly
if not api_key:
    raise ValueError("SARVAM_KEY environment variable is not set. Please check your .env file.")

# Initialize the SarvamAI client
client = SarvamAI(api_subscription_key=api_key)

# Load the JSON file
with open("../data/json/aadiparv_sarvam.json", "r", encoding="utf-8") as file:
    data = json.load(file)

try:
    # Iterate through each verse in the JSON data
    for i, verse in enumerate(data):
        text = verse["text"]  # Extract the text field
        chapter = verse["chapter"] #Extract the chapter field
        verse  = verse["verse"] # Extract the verse number

        response = client.text_to_speech.convert(
                text = text,
                target_language_code="en-IN",
                speaker="ritu",
                pace=1,
                speech_sample_rate=22050,
                enable_preprocessing=False,
                model="bulbul:v3"
        )
        
        audio_data_v3 = base64.b64decode(response.audios[0])
        output_file = f"../outputs/sanskrit/adiparva_{chapter}_{verse}.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data_v3)
        print(f"Audio saved as adiparva_{chapter}_{verse}.wav")   
    
    
except Exception as e:
    print(f"Text-to-speech conversion failed: {e}")
