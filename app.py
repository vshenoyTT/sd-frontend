import streamlit as st
import requests
from PIL import Image
import io
import time

# Replace with your VM's IP address or domain name
SERVER_URL = "http://10.229.36.110:5000"

st.title("TT Stable Diffusion Image Generator")

# User input
prompt = st.text_input("Enter your prompt:", "A beautiful landscape with mountains and a lake")

# Generate button
if st.button("Generate Image"):
    with st.spinner("Generating image... This may take a while."):
        try:
            # Prepare the request data
            data = {"prompt": prompt}
            
            # Send request to add the prompt to the server
            response = requests.post(f"{SERVER_URL}/submit", json=data)
            
            if response.status_code == 200:
                st.success("Prompt added successfully! Waiting for the image to be generated...")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")


st.markdown("---")
st.write("This app generates images using Stable Diffusion running on Wormhole N150.")
