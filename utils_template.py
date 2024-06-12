import fitz
from langchain.document_loaders import UnstructuredFileLoader

def crop_pdf(input_pdf, output_pdf, left, top, width, height):
    # Open the PDF
    pdf_document = fitz.open(input_pdf)

    # Iterate through each page and crop it
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page.set_cropbox(fitz.Rect((left, top, left + width, top + height)))
        page.get_textpage(clip=(left, top, width, height))

    # Save the modified PDF
    pdf_document.save(output_pdf)
    pdf_document.close()

def process_uploaded_files(uploaded_files):
    documents = []
    metadata = []
    for uploaded_file in uploaded_files:
        loader = UnstructuredFileLoader(uploaded_file)
        loaded_documents = loader.load()
        documents.append(loaded_documents[0].page_content)
        metadata.append({"title":loaded_documents[0].metadata['source']})
    return documents, metadata
