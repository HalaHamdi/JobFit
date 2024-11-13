import streamlit as st
from styles import load_css,color_palette
from utils import resume_and_jd_uploader,match_resumes, side_bar, display_matched_resumes

st.set_page_config(page_title="Resume Matcher", layout="wide")

# # Load custom CSS
st.markdown(load_css(),unsafe_allow_html=True)

# # App Title with custom color
st.markdown("<h1 class='section-header'>Resume Matcher</h1>", unsafe_allow_html=True)


uploaded_files,job_description=resume_and_jd_uploader(st)

# A horizontal divider to separate sections
st.markdown("<hr>", unsafe_allow_html=True)

match_resumes(st,uploaded_files,job_description)
display_matched_resumes(st)

top_k_req=side_bar(st)

    