import os
import requests
import base64
import streamlit_ext as ste


def local_audio_generation(prompt, epochs, seed, url):
    """
    Generates an audio file from a given prompt using a specified API.

    Parameters:
    prompt (str): The input prompt for generating audio.
    epochs (int): The number of inference steps.
    seed (str): The seed image ID for reproducibility.
    url (str): The API endpoint URL.

    Returns:
    None

    The function sends a POST request to the given URL with the specified parameters,
    receives a Base64-encoded audio string in response, decodes it, and saves it as a .wav file.
    """

    # Define the payload for the POST request
    payload = {
      "alpha": 0,
      "num_inference_steps": epochs,
      "seed_image_id": seed,

      "start": {
        "prompt": prompt,
        "seed": 42,
        "denoising": 0.75,
        "guidance": 7.0
      },

      "end": {
        "prompt": prompt,
        "seed": 123,
        "denoising": 0.75,
        "guidance": 7.0
      }
    }

    # Make the POST request
    response = requests.post(url, json=payload)
    response_dict = response.json()
    print(response_dict)
    print(type(response_dict))

    # Base64-encoded audio string
    audio_base64 = response_dict['audio']

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

    print("Audio file saved as gen_sound.wav")


def download(file, mim, label):
    """
    Provides a download button for a specified file in a Streamlit application.

    Parameters:
    file (str): The path to the file to be downloaded.
    mim (str): The MIME type of the file.
    label (str): The label for the download button.

    Returns:
    None

    The function opens the specified file in binary mode, reads its content,
    and uses Streamlit's download_button to allow users to download the file.
    """
    with open(file, 'rb') as out_file:
        ste.download_button(
            label=label,
            data=out_file,
            file_name=os.path.basename(file),
            mime=mim
        )

