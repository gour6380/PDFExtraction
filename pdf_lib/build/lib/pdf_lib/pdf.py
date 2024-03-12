#Importing necessary libraries
from pdfminer.layout import LAParams
from pdfminer.high_level import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFPasswordIncorrect
from pdfminer.pdfparser import PDFParser
import io
import re
import PyPDF2
import warnings
import json
warnings.filterwarnings("ignore")

def process_pdf(buffer, password=None):
    """
    Processes a PDF file from a given buffer, decrypting it if necessary.

    Parameters:
    buffer (BytesIO): An in-memory buffer containing PDF data.
    password (str, optional): Password for decrypting the PDF, if it is encrypted.

    Returns:
    dict: Processed text from the PDF or an error message.

    The function decrypts the PDF if it's encrypted and a password is provided, and then extracts text from it.
    """
    reader = PyPDF2.PdfReader(buffer)
    if reader.is_encrypted and password:
        if reader.decrypt(password):
            buffer = io.BytesIO()
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.write(buffer)
            buffer.seek(0)
    return extract_text(buffer)

def extract_text(buffer):
    """
    Extracts text from a PDF file contained in a buffer.

    Parameters:
    buffer (BytesIO): An in-memory buffer containing PDF data.

    Returns:
    dict: If successful, returns extracted text. If an error occurs, returns an error message.

    The function reads from a buffer containing PDF data and extracts text, handling any exceptions that occur.
    """
    try:
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    
        for page in PDFPage.get_pages(buffer, caching=True, check_extractable=False):
            page_interpreter.process_page(page)
                            
        text = fake_file_handle.getvalue()
        text_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\u0080-\uFFFF]')
        text = text_pattern.sub('', text)

        converter.close()
        return json.dumps({"success": True, "text": text})
    except PDFPasswordIncorrect as e:
        return json.dumps({"success": False, "text": "Password is incorrect"})
    except Exception as e:
        return json.dumps({"success": False, "text": str(e)})
