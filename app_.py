import fitz  # PyMuPDF
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        # Procesar el archivo PDF usando fitz
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        
        # Inicializar variables para almacenar la información
        data = {
            "condicionesPago": "",
            "emisorNombre": "",
            "emisorRfc": "",
            "fechaEmision": "",
            "fechaTimbrado": "",
            "flt_e_dom": "",
            "flt_flete": "",
            "flt_m_car": "",
            "flt_m_des": "",
            "flt_o_lin": "",
            "flt_rec": "",
            "flt_seg": "",
            "folio": "",
            "formaPago": "",
            "iva": "",
            "receptorNombre": "",
            "receptorRfc": "",
            "ret_iva": "",
            "status": "",
            "subtotal": "",
            "tipoMoneda": "",
            "tipoPago": "",
            "total": "",
            "uuid": ""
        }

        # Extraer texto de cada página
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()

            # Buscar patrones específicos en el texto
            if not data["emisorNombre"]:
                match = re.search(r'Nombre emisor:\s*(.*)', text)
                if match:
                    data["emisorNombre"] = match.group(1).strip()

            if not data["emisorRfc"]:
                match = re.search(r'RFC emisor:\s*(.*)', text)
                if match:
                    data["emisorRfc"] = match.group(1).strip()

            if not data["receptorNombre"]:
                match = re.search(r'Nombre receptor:\s*(.*)', text)
                if match:
                    data["receptorNombre"] = match.group(1).strip()

            if not data["receptorRfc"]:
                match = re.search(r'RFC receptor:\s*(.*)', text)
                if match:
                    data["receptorRfc"] = match.group(1).strip()

            if not data["folio"]:
                match = re.search(r'Folio fiscal:\s*(.*)', text)
                if match:
                    data["folio"] = match.group(1).strip()

            if not data["uuid"]:
                match = re.search(r'UUID\s*:\s*(.*)', text)
                if match:
                    data["uuid"] = match.group(1).strip()

            if not data["subtotal"]:
                match = re.search(r'SUBTOTAL\s*:\s*\$?\s*(.*)', text)
                if match:
                    data["subtotal"] = match.group(1).strip()

            if not data["total"]:
                match = re.search(r'TOTAL\s*:\s*\$?\s*(.*)', text)
                if match:
                    data["total"] = match.group(1).strip()

            if not data["formaPago"]:
                match = re.search(r'FORMA DE PAGO\s*:\s*(.*)', text)
                if match:
                    data["formaPago"] = match.group(1).strip()

            if not data["tipoMoneda"]:
                match = re.search(r'TIPO DE MONEDA\s*:\s*(.*)', text)
                if match:
                    data["tipoMoneda"] = match.group(1).strip()

            if not data["tipoPago"]:
                match = re.search(r'TIPO DE PAGO\s*:\s*(.*)', text)
                if match:
                    data["tipoPago"] = match.group(1).strip()

            if not data["condicionesPago"]:
                match = re.search(r'CONDICIONES DE PAGO\s*:\s*(.*)', text)
                if match:
                    data["condicionesPago"] = match.group(1).strip()

            if not data["fechaEmision"]:
                match = re.search(r'FECHA Y HORA DE EMISION\s*:\s*(.*)', text)
                if match:
                    data["fechaEmision"] = match.group(1).strip()

            if not data["fechaTimbrado"]:
                match = re.search(r'FECHA Y HORA DE CERTIFICACION\s*:\s*(.*)', text)
                if match:
                    data["fechaTimbrado"] = match.group(1).strip()

            if not data["flt_flete"]:
                match = re.search(r'FLT-FLETE\s*:\s*(.*)', text)
                if match:
                    data["flt_flete"] = match.group(1).strip()

            if not data["flt_seg"]:
                match = re.search(r'FLT-SEG\s*:\s*(.*)', text)
                if match:
                    data["flt_seg"] = match.group(1).strip()

            if not data["flt_o_lin"]:
                match = re.search(r'FLT-O. LIN\s*:\s*(.*)', text)
                if match:
                    data["flt_o_lin"] = match.group(1).strip()

            if not data["flt_rec"]:
                match = re.search(r'FLT-REC\s*:\s*(.*)', text)
                if match:
                    data["flt_rec"] = match.group(1).strip()

            if not data["flt_e_dom"]:
                match = re.search(r'FLT-E. DOM\s*:\s*(.*)', text)
                if match:
                    data["flt_e_dom"] = match.group(1).strip()

            if not data["flt_m_car"]:
                match = re.search(r'FLT-M. CAR\s*:\s*(.*)', text)
                if match:
                    data["flt_m_car"] = match.group(1).strip()

            if not data["flt_m_des"]:
                match = re.search(r'FLT-M. DES\s*:\s*(.*)', text)
                if match:
                    data["flt_m_des"] = match.group(1).strip()

            if not data["iva"]:
                match = re.search(r'IVA\s*:\s*\$?\s*(.*)', text)
                if match:
                    data["iva"] = match.group(1).strip()

            if not data["ret_iva"]:
                match = re.search(r'RET. IVA\s*:\s*\$?\s*(.*)', text)
                if match:
                    data["ret_iva"] = match.group(1).strip()

        # Cerrar el documento PDF
        pdf_document.close()

        # Retornar la información extraída en la respuesta
        return jsonify(data), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
