import streamlit as st
import requests
from PIL import Image
import io
import time
import os

DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "generated_image.png")

# Add space below the title
st.title("TT Stable Diffusion Playground")
st.markdown("<br>", unsafe_allow_html=True)

# Display an image logo at the end of the title

# Popover for Device ID input
with st.expander("Add Device ID"):
    device_id = st.text_input("What's your device ID? 10.229.36.110")

st.markdown("<br>", unsafe_allow_html=True)

prompt = st.text_input("Enter your prompt:", "")

# Function to save image to Downloads and display it
def save_and_display_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        image.save(DOWNLOAD_PATH)
        image_placeholder.image(image, caption="Generated Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error processing image: {e}")

# Placeholder for the image
image_placeholder = st.empty()

# Function to check and update the image
def check_and_update_image(server_url):
    try:
        image_response = requests.get(f"{server_url}/get_image")
        if image_response.status_code == 200 and image_response.content:
            save_and_display_image(image_response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {e}")

# Button to generate the image
if st.button("Generate Image"):
    if not device_id:
        st.error("Please enter your device ID.")
    else:
        SERVER_URL = f"http://{device_id}:5000"
        with st.spinner("Running Stable Diffusion"):
            try:
                data = {"prompt": prompt}
                response = requests.post(f"{SERVER_URL}/submit", json=data)
                if response.status_code != 200:
                    st.error(f"Error submitting prompt: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the server: {e}")
            else:
                while True:
                    check_and_update_image(SERVER_URL)
                    time.sleep(2)

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
