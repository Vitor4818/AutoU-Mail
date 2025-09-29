from flask import Blueprint, render_template, request, flash, session
from services.email_service import process_email
from services.file_service import extract_text_from_file

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    email_text = ""

    # garante que session["history"] sempre existe
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        email_text = request.form.get("email_text", "").strip()
        uploaded_file = request.files.get("email_file")

        if uploaded_file and uploaded_file.filename:
            file_text = extract_text_from_file(uploaded_file)
            if file_text:
                email_text = file_text
                flash(f"Arquivo '{uploaded_file.filename}' carregado com sucesso!", "success")

        if email_text:
            result = process_email(email_text)

            # insere no topo do histórico do usuário
            history = session["history"]
            history.insert(0, result)
            session["history"] = history
        else:
            result = {"email": "", "categoria": "Indefinido", "resposta": "Nenhum email fornecido."}

    return render_template("index.html", result=result, email_text=email_text, history=session.get("history", []))
