# Local PDF to Markdown RAG Solution
This Streamlit application processes PDF documents, analyzes each page using AI, extracts and formats the data, and then outputs the content in Markdown format, ready for indexing.
Im building this because during my first attempts to build Document Rag's in 2024, I realised that preparing the data for indexing was a painful and time consuming process. I wanted to make it easier for myself, and others, to do this. Also if the source data is not well formatted for indexing, sometimes the results can be funny.

Challenges 
- PDFs are not always well formatted for indexing.
- Tables are sometimes formmatted differently in 1 document compared to another document
- Images are sometimes made with wordart shapes, when we use python to extract these, it does not usually go so well
- Sometimes data in 1 pdf can be repeated in another pdf but with a slight difference poisoning the results
- Relying on a scrpt to index 1 pdf according to ruleselts works fine, 2500 all formatted differently however I found presented problems of consostency, if i patched the script to fix 1 document, something else broke

Solution
I want to build a POC utility that allows a user to upload a single PDF, I then want to analyse each page, identify what are paragraphs, what are tables, what are images, what are headings, then I want to extract all that data into markdown, Then I want AI to look at whats been extracted and fill in any gaps or issues that have occured due to formatting

## Features

- **PDF Upload:** Allows users to upload PDF documents.
- **AI-Powered Analysis:** Utilizes AI to analyze each page of the PDF, identifying paragraphs, tables, images, and headings. It also uses AI to fill in any gaps or fix formatting issues that may occur during extraction.
- **Data Extraction:** Extracts relevant data from the analyzed pages.
- **Markdown Output:** Formats the extracted data into Markdown for easy indexing and readability.

## Input and Output

**Input:** A PDF file.

**Output:** A Markdown file containing the extracted and formatted content from the PDF.

## Challenges

This project aims to address the following challenges:

- PDFs are not always well formatted for indexing.
- Tables are sometimes formatted differently in one document compared to another.
- Images are sometimes created with word art shapes, which are difficult to extract using Python.
- Data in one PDF can be repeated in another PDF with slight differences, which can poison the results.
- Relying on a script to index one PDF according to rulesets works fine, but indexing many PDFs with different formats presents problems of consistency.

## How to Use

1.  Upload a PDF file using the file uploader.
2.  The application will process the PDF, analyze each page, and extract the data.
3.  The extracted data will be formatted into Markdown and displayed.

## Project Structure

The project is structured as follows:

-   `app.py`: The main Streamlit application file.
-   `utils.py`: Contains utility functions for PDF processing and AI analysis.
-   `requirements.txt`: Lists the project dependencies.

## Dependencies

-   streamlit
-   PyPDF2
-   (Other AI/ML libraries used for analysis)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    ```
2.  Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```
3.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the Streamlit application:

```bash
streamlit run app.py
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License.
