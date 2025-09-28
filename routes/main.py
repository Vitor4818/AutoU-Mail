from flask import Blueprint, render_template, request, flash
from services.email_service import process_email
from services.file_service import extract_text_from_file

#Cria um blueprint para organizar as rotas
main_bp = Blueprint("main", __name__)

#Histórico em memória dos emails processados
history = []

@main_bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    email_text = ""

    if request.method == "POST":
        #Pega o texto do email enviado pelo formulário
        email_text = request.form.get("email_text", "").strip()
        #Pega arquivo enviado (txt ou pdf)
        uploaded_file = request.files.get("email_file")

        if uploaded_file and uploaded_file.filename:
            #Extrai texto do arquivo
            file_text = extract_text_from_file(uploaded_file)
            if file_text:
                email_text = file_text
                flash(f"Arquivo '{uploaded_file.filename}' carregado com sucesso!", "success")

        if email_text:
            #Processa email: classifica e gera resposta
            result = process_email(email_text)
            history.insert(0, result)  # Adiciona no topo do histórico
        else:
            result = {"email": "", "categoria": "Indefinido", "resposta": "Nenhum email fornecido."}

    #Renderiza template passando resultado, texto do email e histórico
    return render_template("index.html", result=result, email_text=email_text, history=history)
