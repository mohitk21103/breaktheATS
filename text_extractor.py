import PyPDF2
import docx2txt

class FileTextExtractor:
    """
    This class handles text extraction from different file formats like PDF, DOCX, and TXT.
    """

    @staticmethod
    def extract_text_from_pdf(file_path):
        """ Extracts text from a PDF file """
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def extract_text_from_docx(file_path):
        """ Extracts text from a DOCX file """
        return docx2txt.process(file_path)

    @staticmethod
    def extract_text_from_txt(file_path):
        """ Extracts text from a TXT file """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def extract_text(file_path):
        """ Determines the file type and extracts text accordingly """
        if file_path.endswith('.pdf'):
            return FileTextExtractor.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return FileTextExtractor.extract_text_from_docx(file_path)
        elif file_path.endswith('.txt'):
            return FileTextExtractor.extract_text_from_txt(file_path)
        else:
            return ""  # Returns empty if file type is unsupported
