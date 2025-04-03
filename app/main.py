# import streamlit as st
# from scraper import get_relevant_links, scrape_text
# from pdf_processor import extract_text_from_pdf
# from embeddings import store_text_in_supabase, get_relevant_text
# from gemini_ai import ask_gemini
# from supabase import create_client
# import os
# import io
# import uuid
# from dotenv import load_dotenv

# load_dotenv()

# # Supabase Client Setup
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# BUCKET_NAME = "pdf"
# TEMP_FOLDER = "temp_pdfs" 

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# def upload_to_supabase(uploaded_file):
#     """Uploads a PDF file to Supabase Storage and returns the public URL."""

#     file_name = uploaded_file.name  
#     temp_path = os.path.join(TEMP_FOLDER, file_name)  

#     # Save the file as a temporary file
#     with open(temp_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Define the storage path inside Supabase
#     unique_id = uuid.uuid4().hex[:8]  # Generate a short unique ID
#     file_path = f"{unique_id}_pdfs/{file_name}"
    

#     # Upload the file
#     res = supabase.storage.from_(BUCKET_NAME).upload(file_path, temp_path, file_options={"content-type": "application/pdf"})

#     # Check if the upload was successful
#     if hasattr(res, "error") and res.error:
#         raise Exception(f"Upload failed: {res.error}")

#     # Get the public URL of the uploaded file
#     file_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

#     # Delete the temporary file after upload
#     os.remove(temp_path)

#     return file_url
# with st.sidebar:
#     st.title("📄 PDF & Web Content Q&A App")

#     option = st.radio("Select input type:", ("Upload PDFs", "Enter Website URL"))
#     os.makedirs(TEMP_FOLDER, exist_ok=True)
# # 📂 File Upload Section
#     if option == "Upload PDFs":
#         uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

#         if uploaded_files and st.button("📤 Process PDFs"):
#             with st.spinner("Processing PDFs..."):

#                 # ✅ Delete previous embeddings at the start of a new batch upload
            
#                 supabase.table("chunks").delete().neq("sentence", "").execute()
#                 supabase.table("pdf_files").delete().neq("file_name", "").execute()
#                 for uploaded_file in uploaded_files:
#                     pdf_text = extract_text_from_pdf(uploaded_file)
#                     file_url = upload_to_supabase(uploaded_file)
#                     st.markdown(f"✅ Uploaded: [{uploaded_file.name}]({file_url})", unsafe_allow_html=True)

#                     if file_url:
#                         # Store file metadata in `pdf_files` table
#                         supabase.table("pdf_files").insert({"file_name": uploaded_file.name, "file_url": file_url}).execute()

#                         # ✅ Store embeddings for each PDF
#                         store_text_in_supabase(pdf_text, uploaded_file.name, file_url)

#             st.success("✅ PDFs uploaded and processed successfully!")


#     # 🌐 Web Scraping Section
#     elif option == "Enter Website URL":
#         domain_url = st.text_input("Enter website URL:")
#         supabase.table("chunks").delete().neq("sentence", "").execute()
#         if domain_url and st.button("🔍 Scrape Website"):
#             with st.spinner("Scraping website..."):
#                 relevant_pages = get_relevant_links(domain_url)
#                 web_text = scrape_text(relevant_pages)
#                 store_text_in_supabase(web_text, "Website Content", domain_url)

#             st.success("✅ Website content processed successfully!")


# st.subheader("💬 Ask a Question")

# question = st.text_input("Enter your question:")
# if st.button("🔎 Get Answer"):
#     if question:
#         with st.spinner("Searching for relevant information..."):
#             results = get_relevant_text(question)
#             answer = ask_gemini(question, results)
#         if answer:
#             st.write("### 🗣️ Answer:")
#             st.write(answer)
#             if results:
#                 for result in results:
#                     st.markdown(f"📄 **Source:** [{result['file_name']}]({result['file_url']})", unsafe_allow_html=True)
#                     break
#             else:
#                 st.write("❌ No relevant information found.")
#         else:
#             st.write("❌ No answer found.")



import streamlit as st
from scraper import get_relevant_links, scrape_text
from pdf_processor import extract_text_from_pdf
from embeddings import store_text_in_supabase, get_relevant_text
from gemini_ai import ask_gemini
from supabase import create_client
import os
import io
import uuid
from dotenv import load_dotenv

load_dotenv()

# Supabase Client Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "pdf"
TEMP_FOLDER = "temp_pdfs" 

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
st.set_page_config(page_title="PDF & Web Content Q&A App", page_icon="📄")

def upload_to_supabase(uploaded_file):
    """Uploads a PDF file to Supabase Storage and returns the public URL."""
    file_name = uploaded_file.name  
    temp_path = os.path.join(TEMP_FOLDER, file_name)  

    # Save the file as a temporary file
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Define the storage path inside Supabase
    unique_id = uuid.uuid4().hex[:8]  # Generate a short unique ID
    file_path = f"{unique_id}_pdfs/{file_name}"
    
    # Upload the file
    res = supabase.storage.from_(BUCKET_NAME).upload(file_path, temp_path, file_options={"content-type": "application/pdf"})

    # Check if the upload was successful
    if hasattr(res, "error") and res.error:
        raise Exception(f"Upload failed: {res.error}")

    # Get the public URL of the uploaded file
    file_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

    # Delete the temporary file after upload
    os.remove(temp_path)

    return file_url

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.title("📄 PDF & Web Content Q&A App")

    option = st.radio("Select input type:", ("Upload PDFs", "Enter Website URL"))
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # 📂 File Upload Section
    if option == "Upload PDFs":
        uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

        if uploaded_files and st.button("📤 Process PDFs"):
            with st.spinner("Processing PDFs..."):
                # ✅ Delete previous embeddings at the start of a new batch upload
                supabase.table("chunks").delete().neq("sentence", "").execute()
                supabase.table("pdf_files").delete().neq("file_name", "").execute()
                for uploaded_file in uploaded_files:
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    file_url = upload_to_supabase(uploaded_file)
                    st.markdown(f"✅ Uploaded: [{uploaded_file.name}]({file_url})", unsafe_allow_html=True)

                    if file_url:
                        # Store file metadata in `pdf_files` table
                        supabase.table("pdf_files").insert({"file_name": uploaded_file.name, "file_url": file_url}).execute()

                        # ✅ Store embeddings for each PDF
                        store_text_in_supabase(pdf_text, uploaded_file.name, file_url)

            st.success("✅ PDFs uploaded and processed successfully!")

    # 🌐 Web Scraping Section
    elif option == "Enter Website URL":
        domain_url = st.text_input("Enter website URL:")
      
        if domain_url and st.button("🔍 Scrape Website"):
            with st.spinner("Scraping website..."):
                supabase.table("chunks").delete().neq("sentence", "").execute()
                relevant_pages = get_relevant_links(domain_url)
                web_text = scrape_text(relevant_pages)
                store_text_in_supabase(web_text, "Website Content", domain_url)

            st.success("✅ Website content processed successfully!")
# Display chat history
if st.session_state.chat_history:
    st.subheader("🗨️ Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"**Q:** {chat['question']}")
        st.markdown(f"**A:** {chat['answer']}")
        if chat['results']:
            for result in chat['results']:
                st.markdown(f"📄 **Source:** [{result['file_name']}]({result['file_url']})", unsafe_allow_html=True)
                break
st.subheader("💬 Ask a Question")

question = st.text_input("Enter your question:")
if st.button("🔎 Get Answer"):
    if question:
        with st.spinner("Searching for relevant information..."):
            results = get_relevant_text(question)
            answer = ask_gemini(question, results)

        if answer:
            st.session_state.chat_history.append({"question": question, "answer": answer, "results": results})
            st.write("### 🗣️ Answer:")
            st.write(answer)
            if results:
                for result in results:
                    st.markdown(f"📄 **Source:** [{result['file_name']}]({result['file_url']})", unsafe_allow_html=True)
                    break
            else:
                st.write("❌ No relevant information found.")
        else:
            st.write("❌ No answer found.")

