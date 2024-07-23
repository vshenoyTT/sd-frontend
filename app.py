import streamlit as st
import requests
from PIL import Image
import io
import time

SERVER_URL = "http://10.229.36.110:5000"

st.title("TT Stable Diffusion Image Generator")

prompt = st.text_input("Enter your prompt:", "")

# Placeholder for the image
image_placeholder = st.empty()

# Function to check and update the image
def check_and_update_image():
    try:
        image_response = requests.get(f"{SERVER_URL}/get_image")
        if image_response.status_code == 200 and image_response.content:
            image = Image.open(io.BytesIO(image_response.content))
            image_placeholder.image(image, caption="Generated Image", use_column_width=True)
        else:
            image_placeholder.empty()
    except requests.exceptions.RequestException as e:
        print(e)

# Button to generate the image
if st.button("Generate Image"):
    with st.spinner("Generating image... This may take a while."):
        try:
            data = {"prompt": prompt}
            response = requests.post(f"{SERVER_URL}/submit", json=data)
            if response.status_code != 200:
                st.error(f"Error submitting prompt: {response.status_code} - {response.text}")
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
    time.sleep(3)  # Check every 3 seconds
    check_and_update_image()
