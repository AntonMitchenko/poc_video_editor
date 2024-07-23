import os
import requests
import base64
import streamlit_ext as ste

def local_audio_generation(prompt, epochs, seed, url):

    # Define the payload for the POST request
    payload = {
        "input": {
            "alpha": 0,
            "prompt_a": prompt,
            "denoising": 0.75,
            "seed_image_id": seed,
            "num_inference_steps": epochs
        }
    }

    # Make the POST request
    response = requests.post(url, json=payload)
    response_dict = response.json()
    print(response_dict)

    # Base64-encoded audio string
    audio_base64 = response_dict['output']['audio']

    # Remove the data URL scheme (if present)
    if audio_base64.startswith("data:audio/mpeg;base64,"):
        audio_base64 = audio_base64.replace("data:audio/mpeg;base64,", "")

    # Decode the Base64 string to binary data
    audio_data = base64.b64decode(audio_base64)

    # Write the binary data to a .wav file
    directory_path = "./audio"
    file_name = "gen_sound.wav"
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)

    print("Audio file saved as output.wav")


def download(file, mim):
    with open(file, 'rb') as out_file:
        ste.download_button(
            label="Download Final Video",
            data=out_file,
            file_name=os.path.basename(file),
            mime=mim
        )