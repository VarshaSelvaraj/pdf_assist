import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=genai_api_key)

def ask_gemini(question, context):
    """Queries Gemini AI with context-based prompts."""
    full_prompt = f"""
    You are an AI assistant that generates well-structured answers in a clear and readable format.  

    Based on the following document, answer the question **using proper formatting**:  

    - Use **headings (bold or markdown #)** for different sections.  
    - Use **bullet points** or **numbered lists** where applicable.  
    - Use **short paragraphs** to improve readability.  
    - Highlight key terms using **bold text**.  
    - Ensure the answer is structured properly and easy to understand.  

    ### Document:  
    {context}  

    ### Question:  
    {question}  

    ### Provide the response in a structured format as explained above.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
