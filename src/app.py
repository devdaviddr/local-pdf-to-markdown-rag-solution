import streamlit as st
import tempfile
from typing import Dict, List, Tuple
import fitz
from utils import get_available_models, process_pdf, save_and_encode_pdf, format_text_with_llama, display_pdf_and_results

# Set page configuration
st.set_page_config(layout="wide")

def main() -> None:
    """
    Main function to handle the Streamlit app logic.
    """
    # Sidebar
    with st.sidebar:
        st.title("Select PDF")
        st.caption("Upload a PDF file to view and extract text.")
        
        # PDF file uploader
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        
        # Settings expander at the bottom of the sidebar
        with st.expander("Settings", expanded=True):
            zoom_level = st.slider("Zoom Level", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
            show_images = st.checkbox("Show Image Borders", value=True)
            show_text = st.checkbox("Show Text Borders", value=True)

    # Check if a file is uploaded
    if uploaded_file is None:
        st.warning("Please upload a PDF file using the sidebar.")
    else:
        try:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                pdf_file_path = temp_file.name
            
            doc, page_texts = process_pdf(pdf_file_path, show_text, show_images)
            
            # Save and encode the modified PDF
            modified_pdf_bytes, modified_pdf_base64 = save_and_encode_pdf(doc)
            
            # Display the PDF and results
            display_pdf_and_results(modified_pdf_bytes, modified_pdf_base64, page_texts)
        
        except fitz.FileNotFoundError:
            st.error("The specified PDF file was not found.")
        except fitz.PdfError:
            st.error("An error occurred while processing the PDF.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
