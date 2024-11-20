from streamlit_pdf_viewer import pdf_viewer


def resume_page(go_to_page,st):
    if st.button(label="", on_click=go_to_page, args=("home",), icon=":material/arrow_back:"):
        pass  # The page will change immediately
    # Show the PDF viewer for the selected resume if it's in the session state
    if "selected_pdf" in st.session_state:
        selected_pdf = st.session_state.selected_pdf
        pdf_binary = selected_pdf.read()
        st.write(f"## {selected_pdf.name[:-4]}")
        pdf_viewer(pdf_binary,key=selected_pdf.name)


