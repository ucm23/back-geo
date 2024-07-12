from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re
#import fitz

app = Flask(__name__)
CORS(app)

def extract_info_from_pdf(pdf_stream):
    data = {
        "flt_e_dom": "",
        "flt_flete": "",
        "flt_m_car": "",
        "flt_m_des": "",
        "flt_o_lin": "",
        "flt_rec": "",
        "flt_seg": "",
        "iva": "",
        "ret_iva": "",
        "total": ""
    }

    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            table_data = {
                "flt_flete": re.search(r'FLT-FLETE\s*:\s*([\d,]+\.\d{2})', text),
                "flt_seg": re.search(r'FLT-SEG\.\s*:\s*([\d,]+\.\d{2})', text),
                "flt_o_lin": re.search(r'FLT-O\. LIN\.\s*:\s*([\d,]+\.\d{2})', text),
                "flt_rec": re.search(r'FLT-REC\.\s*:\s*([\d,]+\.\d{2})', text),
                "flt_e_dom": re.search(r'FLT-E\. DOM\.\s*:\s*([\d,]+\.\d{2})', text),
                "flt_m_car": re.search(r'FLT-M\. CAR\.\s*:\s*([\d,]+\.\d{2})', text),
                "flt_m_des": re.search(r'FLT-M\. DES\.\s*:\s*([\d,]+\.\d{2})', text),
                "subtotal": re.search(r'SUBTOTAL\s*:\s*([\d,]+\.\d{2})', text),
                "iva": re.search(r'IVA\s*16%\s*([\d,]+\.\d{2})', text),
                "ret_iva": re.search(r'RET\. IVA*\*\s*4%\s*([\d,]+\.\d{2})', text),
                "total": re.search(r"(?i)TOTAL\s*:?\s*\$?\s*([\d,]+(\.\d{2})?)", text)
            }

            #print(table_data)

            for key, match in table_data.items():
                if match:
                    data[key] = match.group(1).strip()
                    #print(key, match.group(1))
    return data

@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        data = extract_info_from_pdf(file)
        return jsonify(data), 200

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/', methods=['GET'])
def get_route():
    return jsonify({"message": "runnig"}), 200

if __name__ == '__main__':
    print("Running")
    app.run(debug=True)
