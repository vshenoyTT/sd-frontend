import streamlit as st
import requests
from PIL import Image
import io

# Replace with your VM's IP address or domain name
SERVER_URL = "http://10.140.36.52:5000"

st.title("Stable Diffusion Image Generator")

# User input
prompt = st.text_input("Enter your prompt:", "A beautiful landscape with mountains and a lake")

# Generate button
if st.button("Generate Image"):
    with st.spinner("Generating image... This may take a while."):
        try:
            # Prepare the request data
            data = {
                "prompt": prompt,
            }
            
            # Send request to the server
            response = requests.post(f"{SERVER_URL}/generate", json=data)
            
            if response.status_code == 200:
                image_path = response.json()['image_path']
                image_url = f"{SERVER_URL}/images/{image_path}"
                
                # Fetch the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image = Image.open(io.BytesIO(image_response.content))
                    st.image(image, caption="Generated Image", use_column_width=True)
                else:
                    st.error("Failed to fetch the generated image.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")

# Display some information
st.markdown("---")
st.write("This app generates images using Stable Diffusion running on a remote server.")
st.write("Adjust the parameters in the sidebar to customize the generation process.")