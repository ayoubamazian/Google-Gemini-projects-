from dotenv import load_dotenv
load_dotenv()

import os 
import streamlit as st

from PIL import Image
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    reponse = model.generate_content([input, image[0], prompt])
    return reponse.text

def input_image_setup(img):
    if img is not None:
        bytes_data = img.getvalue()

        image_parts = [
            {
                "mime_type": img.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else :
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config("Invoice extractor")
input = st.text_input("Input prompt", key="input")
upload_file = st.file_uploader("Choose an image ....", type=["png", "jpg", "jpeg"])
image=""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload a a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is:")
    st.write(response)