import PyPDF2

#Função para extrair texcto de arquivo .txt ou .PDF
def extract_text_from_file(file):
    """Extrai texto de arquivos .txt ou .pdf"""
    if file.filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    return ""
