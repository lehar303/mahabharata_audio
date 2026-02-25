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

# Extract the first element's text
first_text = data[1]["text"]

try:
    # response0 = client.text.translate(
    #     input="नारायणं नमस्कृत्य नरं चैव नरोत्तमम् देवीं सरस्वतीं चैव ततो जयमुदीरयेत्",
    #     source_language_code="hi-IN",
    #     target_language_code="en-IN",
    #     speaker_gender="Female",
    #     mode="formal",
    #     model="mayura:v1"
    # )
    # # Write the translation to a file
    # output_file = "translation_output.txt"
    # with open(output_file, "w", encoding="utf-8") as file:
    #     file.write(f"Translation: {response0.translated_text}")
    
    # Example with bulbul:v3
    response = client.text_to_speech.convert(
            #text="नारायणं नमस्कृत्य नरं चैव नरोत्तमम् \n देवीं सरस्वतीं चैव ततो जयमुदीरयेत्",
            text = first_text,
            target_language_code="en-IN",
            speaker="ritu",
            pace=1,
            speech_sample_rate=22050,
            enable_preprocessing=False,
            model="bulbul:v3"
    )
    
    audio_data_v3 = base64.b64decode(response.audios[0])  # Decode this too
    with open("../outputs/output_adiparva.wav", "wb") as f:
        f.write(audio_data_v3)
    print("Audio saved as output_adiparva.wav")   
    
    
except Exception as e:
    print(f"Text-to-speech conversion failed: {e}")
