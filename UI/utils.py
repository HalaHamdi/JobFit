import os
import sys
import base64
from styles import color_palette
from langchain_community.document_loaders import PyPDFLoader
from helpers import get_database, record_exists, match
import sys
import subprocess

# subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-pdf-viewer"])
from streamlit_pdf_viewer import pdf_viewer
from pdf2image import convert_from_bytes

def resume_and_jd_uploader(st):
    # # Using tabs to split sections visually
    tabs = st.tabs(["📄 Upload Resumes", "📝 Job Description"])

    # # Resumes Tab
    with tabs[0]:
        st.markdown("<p class='sub-header'>Please upload the resumes in PDF format.</p>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    # # Job Description Tab
    with tabs[1]:
        job_description = st.text_area("Enter the job description", height=100)
        st.markdown("</div>", unsafe_allow_html=True)
    
    return uploaded_files, job_description

def match_resumes(st,uploaded_files,job_description):
    # Placeholder for matching logic
    if st.button('🔍Match Resumes'):
        if len(uploaded_files)==0 or job_description == "":
            st.error("Please upload resumes and enter a job description to match.")
            st.stop()
        
        st.markdown("<h3 class='section-header'>Matched Resumes</h3>", unsafe_allow_html=True)

        # Placeholder code for the logic that matches resumes
        matched_resumes=match(job_description,uploaded_files)
        
         # Store matched resumes in session state to keep them across interactions
        if matched_resumes:
            st.session_state.matched_resumes = matched_resumes
        else:
            st.session_state.matched_resumes = []
        
def display_matched_resumes(st):
    # Display matched resumes from session state
    if "matched_resumes" in st.session_state and st.session_state.matched_resumes:
        # Create a row for each matched resume
        for resume, score in st.session_state.matched_resumes:
            # Create two columns: one for the file name and one for the download button
            col1, col2 = st.columns([3, 1])  # First column for the name, second for the download button

            with col1:
                # Display resume name as a clickable button
                if st.button(resume.name, key=resume.name):
                    # When clicked, show the PDF in the viewer
                    st.session_state.selected_pdf = resume

            with col2:
                # Display download button
                st.download_button(
                    label="Download",
                    data=resume,
                    file_name=resume.name,
                    mime="application/pdf"
                )

        # Show the PDF viewer for the selected resume if it's in the session state
        if "selected_pdf" in st.session_state:
            selected_pdf = st.session_state.selected_pdf
            pdf_binary = selected_pdf.read()
            with st.sidebar:
                pdf_viewer(pdf_binary)
    
def side_bar(st):
    with st.sidebar:
        st.markdown(f"<h1 style='color: {color_palette['navy_blue']};'>Customize</h3>", unsafe_allow_html=True)

        # Initialize the session state variable for the number of top resumes
        if 'top_n_resumes' not in st.session_state:
            st.session_state.top_n_resumes = 5

        # Number input field with increment and decrement buttons
        col = st.columns([1])[0]  # Use one column for the whole section

        with col:
            st.markdown(f"<h4 style='color: {color_palette['navy_blue']};'>Top Resumes</h3>", unsafe_allow_html=True)
            st.session_state.top_n_resumes = st.number_input(
                "",
                min_value=1, 
                max_value=10, 
                value=st.session_state.top_n_resumes, 
                step=1, 
                format="%d",
            )
    return st.session_state.top_n_resumes

