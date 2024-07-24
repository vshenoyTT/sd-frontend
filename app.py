import streamlit as st
import requests
from PIL import Image
import io
import time
import os

SERVER_URL = "http://10.229.36.110:5000"
DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "generated_image.png")

st.title("TT Stable Diffusion Image Generator")

with st.popover("Add Device ID"):
    st.markdown("Device ID")
    name = st.text_input("What's your device ID?")

prompt = st.text_input("Enter your prompt:", "")

# Function to save image to Downloads and display it
def save_and_display_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        image.save(DOWNLOAD_PATH)
        image_placeholder.image(image, caption="Generated Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error processing image: {e}")

# Button to generate the image
if st.button("Generate Image"):
    print("TEST")
    with st.spinner("Generating image... This may take a while."):
        try:
            data = {"prompt": prompt}
            response = requests.post(f"{SERVER_URL}/submit", json=data)
            if response.status_code != 200:
                st.error(f"Error submitting prompt: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")

image_placeholder = st.empty()

# Function to check and update the image
def check_and_update_image():
    try:
        image_response = requests.get(f"{SERVER_URL}/get_image")
        if image_response.status_code == 200 and image_response.content:
            save_and_display_image(image_response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {e}")

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# Continuously check and update the image if it has been generated
while True:
    check_and_update_image()
    time.sleep(2)  # Add a delay to avoid overwhelming the server
