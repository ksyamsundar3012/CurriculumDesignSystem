from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from curriculum_engine import generate_curriculum
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json

app = Flask(__name__)
CORS(app)

# ---------------- Health Endpoint ----------------
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'running'}), 200


# ---------------- Curriculum Generator Endpoint ----------------
@app.route('/api/generate-curriculum', methods=['POST'])
def generate_curriculum_api():
    try:
        data = request.get_json()
        skill = data.get("skill")
        level = data.get("level")
        semesters = int(data.get("semesters"))
        weekly_hours = data.get("weekly_hours")
        industry_focus = data.get("industry_focus")

        result = generate_curriculum(skill, level, semesters, weekly_hours, industry_focus)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- PDF Download Endpoint ----------------
@app.route('/api/download-pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()
    program_name = data.get("program_name", "Curriculum Plan")
    curriculum = data.get("curriculum")

    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle(program_name)

    width, height = letter
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 50, f"{program_name}")
    pdf.setFont("Helvetica", 12)

    y = height - 100
    for semester in curriculum:
        pdf.drawString(50, y, f"Semester {semester['semester']}:")
        y -= 20

        for course in semester['courses']:
            pdf.drawString(70, y, f"Course: {course['name']} ({course['credits']} Credits)")
            y -= 15

            for topic in course['topics']:
                pdf.drawString(90, y, f"- {topic}")
                y -= 12
                if y < 50:
                    pdf.showPage()
                    y = height - 50
        y -= 20

    pdf.save()
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"{program_name}.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
