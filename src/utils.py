import fitz  # PyMuPDF
import base64
import os
from typing import Dict, List, Tuple
import ollama  # Import the Ollama library
import tempfile
import streamlit as st

# Set the Ollama host globally
client = ollama.Client()

def get_available_models() -> List[str]:
    """
    Get a list of available models from Ollama.
    
    Returns:
        List[str]: A list of available model names.
    """
    try:
        # Fetch the list of models from Ollama
        models_response = client.list()
        print(f"Ollama models response: {models_response}")
        
        # Extract model names from the response
        if "models" in models_response and isinstance(models_response["models"], list):
            model_names = [model["model"] for model in models_response["models"]]
            return model_names
        else:
            st.warning("No models found in the Ollama response.")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching available models: {e}")
        return []

def process_pdf(pdf_path: str, show_text: bool, show_images: bool) -> Tuple[fitz.Document, Dict[int, List[str]]]:
    """
    Process the PDF to extract text and draw borders around text blocks and images.
    
    Args:
        pdf_path (str): Path to the PDF file.
        show_text (bool): Whether to draw borders around text blocks.
        show_images (bool): Whether to draw borders around images.
    
    Returns:
        Tuple[fitz.Document, Dict[int, List[str]]]: The processed PDF document and a dictionary of page texts.
    """
    doc = fitz.open(pdf_path)
    page_texts: Dict[int, List[str]] = {}
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_texts[page_num] = []
        
        # Extract and process text blocks
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: (block[1], block[0]))  # Sort by vertical position, then horizontal
        
        for block in blocks:
            if block[6] == 0:  # Check if it's a text block (type 0)
                text = block[4]  # Extract the text content
                page_texts[page_num].append(text)
                
                if show_text:
                    rect = fitz.Rect(block[:4])  # Get the bounding box of the text block
                    page.draw_rect(rect, color=(1, 0, 0), width=1.5)  # Draw a red border
        
        # Draw borders around images
        if show_images:
            for img in page.get_images(full=True):
                bbox = page.get_image_bbox(img)  # Get the bounding box of the image
                page.draw_rect(bbox, color=(0, 0, 1), width=1.5)  # Draw a blue border
    
    return doc, page_texts

def save_and_encode_pdf(doc: fitz.Document) -> Tuple[bytes, str]:
    """
    Save the modified PDF to a temporary file and encode it to base64.
    
    Args:
        doc (fitz.Document): The PDF document to save and encode.
    
    Returns:
        Tuple[bytes, str]: The raw PDF bytes and the base64-encoded string.
    """
    modified_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    doc.save(modified_pdf_path)
    doc.close()
    
    with open(modified_pdf_path, "rb") as f:
        modified_pdf_bytes = f.read()
    return modified_pdf_bytes, base64.b64encode(modified_pdf_bytes).decode("utf-8")

def format_text_with_llama(text: str, model: str) -> str:
    """
    Use the selected Ollama model to format the text into Markdown.
    
    Args:
        text (str): The text to format.
        model (str): The model to use for formatting.
    
    Returns:
        str: The formatted Markdown text.
    """
    try:
        # Send the text to the selected model for formatting
        response = client.generate(
            model=model,
            prompt=f"Format the following text into Markdown without removing any data:\n\n{text}"
        )
        return response["response"]
    except Exception as e:
        st.error(f"An error occurred while formatting the text with {model}: {e}")
        return text  # Return the original text if formatting fails

def display_pdf_and_results(modified_pdf_bytes: bytes, modified_pdf_base64: str, page_texts: Dict[int, List[str]]) -> None:
    """
    Display the modified PDF and extracted results in a two-column layout.
    
    Args:
        modified_pdf_bytes (bytes): The raw PDF bytes for download.
        modified_pdf_base64 (str): The base64-encoded PDF for display.
        page_texts (Dict[int, List[str]]): A dictionary of page texts.
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("PDF Viewer")
        # Display the modified PDF in an iframe
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{modified_pdf_base64}" 
                width="100%" 
                height="800px" 
                style="border: 1px solid #ccc;">
        </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Add a download button for the modified PDF
        st.download_button(
            label="Download Modified PDF",
            data=modified_pdf_bytes,
            file_name="modified_pdf.pdf",
            mime="application/pdf",
        )
    
    with col2:
        st.subheader("Extracted Result")
        # Display the extracted text for each page in expanders
        for page_num, texts in page_texts.items():
            with st.expander(f"Page {page_num + 1}"):
                # Tabs for Extraction and AI Output
                tab1, tab2 = st.tabs(["Extraction", "AI Output"])
                
                with tab1:
                    st.write("\n\n".join(texts))  # Display all text blocks for the page, separated by double newlines
                
                with tab2:
                    # Dropdown to select the model
                    available_models = get_available_models()
                    selected_model = st.selectbox(
                        "Select a model for AI processing",
                        available_models,
                        key=f"model_{page_num + 1}",
                    )
                    
                    prompt = st.text_area(
                        "Enter prompt for AI processing",
                        value="Format the following text into Markdown without removing any data",
                        key=f"prompt_{page_num + 1}",
                    )
                    
                    # Add a button to trigger AI processing
                    if st.button(f"Process Through AI (Page {page_num + 1})"):
                        with st.spinner(f"Processing Page {page_num + 1} through AI..."):
                            # Format the text using the selected model
                            formatted_text = format_text_with_llama(f"{prompt}\n" + "\n\n".join(texts), selected_model)
                            # Add a scrollable container for the AI output
                            st.markdown(
                                f"""
                                <div style="height: 600px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
                                    {formatted_text}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.download_button(
                                label=f"Download Markdown (Page {page_num + 1})",
                                data=formatted_text,
                                file_name=f"page_{page_num + 1}.md",
                                mime="text/markdown",
                            )