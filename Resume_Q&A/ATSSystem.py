from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def check_safety_ratings(response):
    # Assuming `response` is an object that includes safety ratings information
    # The structure and existence of safety ratings might depend on the API's response format
    if hasattr(response, 'candidate') and hasattr(response.candidate, 'safety_ratings'):
        safety_ratings = response.candidate.safety_ratings
        print("Safety Ratings:", safety_ratings)
        # Further processing based on safety ratings
        # This could include logging or handling specific safety flags
    else:
        print("Safety ratings not found in the response.")


def get_gemini_response(input,pdf_cotent):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input, pdf_content[0]])
    check_safety_ratings(response)
    return response.text

def get_gemini_response_for_best_match(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input, pdf_content[0], prompt])
    check_safety_ratings(response)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...")


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt = """
"As a specialist HR professional analyzing this resume, leverage your expertise to provide a comprehensive evaluation. 
Focus on extracting and summarizing key information in a manner that supports decision-making for potential hiring. 
Specifically, detail the following:

1. Applicant’s identity, including full name and contact details.
2. A succinct professional summary or career objective that captures the candidate’s aspirations and strengths.
3. Educational qualifications, highlighting degrees, institutions, and years of completion.
4. A chronological overview of work experience, with emphasis on roles, responsibilities, achievements, and employment durations.
5. A list of skills and proficiencies, particularly those pertinent to the job the candidate is applying for.
6. Any certifications, licenses, or special training that the candidate possesses.
7. Language proficiencies and levels of fluency.
8. References, if provided, with a note on their relevance and the context in which they might be contacted.

Your analysis should not only summarize the content but also provide insights into the candidate’s fit for the role based on the information presented in the resume. Consider the layout, presentation, and any visual cues in the resume as part of your comprehensive review."

"""


# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt,pdf_content)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        if input_text:
            response=get_gemini_response_for_best_match(input_prompt3,pdf_content,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please write job description")
    else:
        st.write("Please uplaod the resume")

   




