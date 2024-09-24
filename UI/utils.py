import os
from langchain_community.document_loaders import PyPDFLoader
from styles import color_palette


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
        st.write(uploaded_files)
        if len(uploaded_files)==0 or job_description == "":
            st.error("Please upload resumes and enter a job description to match.")
            st.stop()
        
        st.markdown("<h3 class='section-header'>Matched Resumes</h3>", unsafe_allow_html=True)

        # Placeholder code for the logic that matches resumes
        dir='./tmp/'
        for i,uploaded_file in enumerate(uploaded_files):  # Placeholder for the number of resumes selected in the sidebar
            tmp_location = os.path.join(dir, uploaded_file.name)

            # if the path does not exist, create the directory and save the file
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(tmp_location, 'wb') as file:
                file.write(uploaded_file.getbuffer())
                
            st.write(tmp_location)
            loader = PyPDFLoader(tmp_location)
            pages = loader.load_and_split()
            
            # delete the file after processing
            os.remove(tmp_location) 
            
            st.markdown(f"<div class='card'>🏆 Matched Resume {i}</div>", unsafe_allow_html=True)
            st.write(f"page 1: {pages[0]}...")  # Replace with actual matched resume text

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