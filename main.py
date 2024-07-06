import fitz  # PyMuPDF
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
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
        emisorNombre = emisorRfc = receptorNombre = receptorRfc = ""
        folio = uuid = subtotal = total = ""
        formaPago = tipoMoneda = tipoPago = condicionesPago = ""
        fechaEmision = fechaTimbrado = status = ""
        flt_flete = flt_seg = flt_o_lin = flt_rec = ""
        flt_e_dom = flt_m_car = flt_m_des = ""
        iva = ret_iva = ""

        # Extraer texto de cada página
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()

            # Buscar patrones específicos en el texto
            if not emisorNombre:
                match = re.search(r'(?i)emisor\s*nombre\s*:\s*(.*)', text)
                if match:
                    emisorNombre = match.group(1).strip()

            if not emisorRfc:
                match = re.search(r'(?i)emisor\s*rfc\s*:\s*(.*)', text)
                if match:
                    emisorRfc = match.group(1).strip()

            if not receptorNombre:
                match = re.search(r'(?i)receptor\s*nombre\s*:\s*(.*)', text)
                if match:
                    receptorNombre = match.group(1).strip()

            if not receptorRfc:
                match = re.search(r'(?i)receptor\s*rfc\s*:\s*(.*)', text)
                if match:
                    receptorRfc = match.group(1).strip()

            if not folio:
                match = re.search(r'(?i)folio\s*fiscal\s*:\s*(.*)', text)
                if match:
                    folio = match.group(1).strip()

            if not uuid:
                match = re.search(r'(?i)uuid\s*:\s*(.*)', text)
                if match:
                    uuid = match.group(1).strip()

            if not subtotal:
                match = re.search(r'(?i)subtotal\s*:\s*\$?\s*(.*)', text)
                if match:
                    subtotal = match.group(1).strip()

            if not total:
                match = re.search(r'(?i)total\s*:\s*\$?\s*(.*)', text)
                if match:
                    total = match.group(1).strip()

            if not formaPago:
                match = re.search(r'(?i)forma\s*pago\s*:\s*(.*)', text)
                if match:
                    formaPago = match.group(1).strip()

            if not tipoMoneda:
                match = re.search(r'(?i)tipo\s*moneda\s*:\s*(.*)', text)
                if match:
                    tipoMoneda = match.group(1).strip()

            if not tipoPago:
                match = re.search(r'(?i)tipo\s*pago\s*:\s*(.*)', text)
                if match:
                    tipoPago = match.group(1).strip()

            if not condicionesPago:
                match = re.search(r'(?i)condiciones\s*pago\s*:\s*(.*)', text)
                if match:
                    condicionesPago = match.group(1).strip()

            if not fechaEmision:
                match = re.search(r'(?i)fecha\s*emision\s*:\s*(.*)', text)
                if match:
                    fechaEmision = match.group(1).strip()

            if not fechaTimbrado:
                match = re.search(r'(?i)fecha\s*timbrado\s*:\s*(.*)', text)
                if match:
                    fechaTimbrado = match.group(1).strip()

            if not status:
                match = re.search(r'(?i)status\s*:\s*(.*)', text)
                if match:
                    status = match.group(1).strip()

            if not flt_flete:
                match = re.search(r'FLT-FLETE\s*:\s*(.*)', text)
                if match:
                    flt_flete = match.group(1).strip()

            if not flt_seg:
                match = re.search(r'FLT-SEG\s*:\s*(.*)', text)
                if match:
                    flt_seg = match.group(1).strip()

            if not flt_o_lin:
                match = re.search(r'FLT-O. LIN\s*:\s*(.*)', text)
                if match:
                    flt_o_lin = match.group(1).strip()

            if not flt_rec:
                match = re.search(r'FLT-REC\s*:\s*(.*)', text)
                if match:
                    flt_rec = match.group(1).strip()

            if not flt_e_dom:
                match = re.search(r'FLT-E. DOM\s*:\s*(.*)', text)
                if match:
                    flt_e_dom = match.group(1).strip()

            if not flt_m_car:
                match = re.search(r'FLT-M. CAR\s*:\s*(.*)', text)
                if match:
                    flt_m_car = match.group(1).strip()

            if not flt_m_des:
                match = re.search(r'FLT-M. DES\s*:\s*(.*)', text)
                if match:
                    flt_m_des = match.group(1).strip()

            if not iva:
                match = re.search(r'IVA\s*:\s*(.*)', text)
                if match:
                    iva = match.group(1).strip()

            if not ret_iva:
                match = re.search(r'RET. IVA\s*:\s*(.*)', text)
                if match:
                    ret_iva = match.group(1).strip()

        # Cerrar el documento PDF
        pdf_document.close()

        # Retornar la información extraída en la respuesta
        return jsonify({
            "emisorNombre": emisorNombre,
            "emisorRfc": emisorRfc,
            "receptorNombre": receptorNombre,
            "receptorRfc": receptorRfc,
            "folio": folio,
            "uuid": uuid,
            "subtotal": subtotal,
            "total": total,
            "formaPago": formaPago,
            "tipoMoneda": tipoMoneda,
            "tipoPago": tipoPago,
            "condicionesPago": condicionesPago,
            "fechaEmision": fechaEmision,
            "fechaTimbrado": fechaTimbrado,
            "status": status,
            "flt_flete": flt_flete,
            "flt_seg": flt_seg,
            "flt_o_lin": flt_o_lin,
            "flt_rec": flt_rec,
            "flt_e_dom": flt_e_dom,
            "flt_m_car": flt_m_car,
            "flt_m_des": flt_m_des,
            "iva": iva,
            "ret_iva": ret_iva
        }), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
