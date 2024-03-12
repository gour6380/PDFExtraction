from .pdf import process_pdf
import io
import json

def main(pythonData, password=None):
    """
    Processes a PDF from binary data, optionally using a password.

    Parameters:
    pythonData (bytes): Binary data of the PDF.
    password (str, optional): Password for the PDF, if needed.

    Returns:
    dict: If successful, returns processed data. If an error occurs, returns an error message.

    The function reads binary data of a PDF, processes it, and handles exceptions.
    """
    o ="{"
    c="}"
    try:
        buffer = io.BytesIO(pythonData)
        return process_pdf(buffer, password=password)
    except Exception as e:
        return json.dumps({"success": False, "text": str(e)})
