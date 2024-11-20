import streamlit as st
from components.home import home_page
from components.resume import resume_page
from styles import load_css,color_palette


# # Load custom CSS
st.markdown(load_css(),unsafe_allow_html=True)

# Set up session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default to the home page
    
# Function to change pages
def go_to_page(page_name):
    st.session_state.page = page_name

# Navigation logic
if st.session_state.page == "home":
    home_page(go_to_page,st)
elif st.session_state.page == "resume":
    resume_page(go_to_page,st)
