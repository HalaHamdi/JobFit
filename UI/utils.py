import os
import sys
import base64
from styles import color_palette
from langchain_community.document_loaders import PyPDFLoader
from helpers import get_database, record_exists, match
import sys
import subprocess
import time
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
        
        
        top_k=st.session_state.top_n_resumes

        # Placeholder code for the logic that matches resumes
        matched_resumes=match(job_description,uploaded_files,top_k,st)
        
         # Store matched resumes in session state to keep them across interactions
        if matched_resumes:
            st.session_state.matched_resumes = matched_resumes
        else:
            st.session_state.matched_resumes = []
def display_matched_resumes(st):
    # Display matched resumes from session state
    if "matched_resumes" in st.session_state and st.session_state.matched_resumes:
      # Create a row for each matched resume
      st.markdown("<h1 class='section-header'>Matched Resumes</h1>", unsafe_allow_html=True)
      for index, (resume, score) in enumerate(st.session_state.matched_resumes, start=1):
        # Create two columns: one for the order number and name, the other for the download button
        col1, col2, col3,col4 = st.columns([1, 2, 1, 1])  # Adjust the column widths as needed

        with col1:
            # Display the order number
            styled_number = f"""
                <div style="
                    background-color: #ff71ce;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    text-align: center;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    display: inline-block;
                    line-height: 30px;">
                    {index}
                </div>
                """
            st.markdown(styled_number, unsafe_allow_html=True)

        with col2:
            # resume_name, extension = os.path.splitext(resume.name)
            # Display resume name as a clickable button
            if st.button(label=resume.name[:-4], key= f"btn_{resume.name}", icon=":material/picture_as_pdf:"):
                # When clicked, show the PDF in the viewer
                st.session_state.selected_pdf = resume

        with col3:
             # Format the score to two decimal places and add a "%" symbol
            formatted_score = f"{score*100:.1f}%"
            # Display the score with the same style as the order number
            styled_score = f"""
                <div style="
                    background-color: #ff71ce;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    text-align: center;
                    border-radius: 10%;
                    width: 60px;  /* Adjust width to fit score and % */
                    height: 60px;  /* Adjust height to maintain circular shape */
                    display: inline-block;
                    line-height: 60px;">
                    {formatted_score}
                </div>
                """
            st.markdown(styled_score, unsafe_allow_html=True)
            
        with col4:
            # Display download button
            st.download_button(
                label="",
                icon=":material/download:",
                data=resume,
                file_name=resume.name,
                mime="application/pdf",
                key=f"download_{resume.name}"
                
            )

    # Show the PDF viewer for the selected resume if it's in the session state
    if "selected_pdf" in st.session_state:
        selected_pdf = st.session_state.selected_pdf
        pdf_binary = selected_pdf.read()
        with st.sidebar:
            pdf_viewer(pdf_binary,key=selected_pdf.name)
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
            top_n_resumes = st.number_input(
                "",
                min_value=1, 
                max_value=10, 
                value=st.session_state.top_n_resumes, 
                step=1, 
                format="%d",
            )

            # Update session state only if the value has changed
            if top_n_resumes != st.session_state.top_n_resumes:
                st.session_state.top_n_resumes = top_n_resumes

