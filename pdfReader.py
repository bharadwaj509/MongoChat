import fitz  # Import PyMuPDF


def extract_paragraphs(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs = []  # List to hold paragraphs

    for page in doc:  # Iterate through each page
        print(page)
        blocks = page.get_text("blocks")  # Get text blocks from the page
        for block in blocks:
            text = block[4].strip()  # Extract text from block

            # Simple heuristic to identify a paragraph (customize as needed):
            # For example, check if the block of text has more than a certain number of characters
            # This is a very basic filter and might need adjustment
            if len(text) > 100:  # Assuming paragraphs typically have more than 100 characters
                paragraphs.append(text)

    doc.close()
    return paragraphs


pdf_path = 'intro.pdf'  # Path to your PDF file
paragraphs = extract_paragraphs(pdf_path)

# Print extracted paragraphs
# for para in paragraphs:
#     print(para, "\n")