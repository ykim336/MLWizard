from mlwizards import extract_pdf, preprocess_text

pdf_path = "datasets/lamedeer.pdf"
extracted_text = extract_pdf(pdf_path)
print(extracted_text)