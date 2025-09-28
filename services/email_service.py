from google import genai
from utils.preprocess import preprocess_text
import re
import os

#API key via variável de ambiente

api_key = os.getenv("GENAI_API_KEY")  #pega a chave da variável de ambiente
if not api_key:
    raise ValueError("Variável de ambiente GENAI_API_KEY não definida!")

client = genai.Client(api_key=api_key)

#Palavras chaves para detectar uum email produtivo
keywords_produtivo = ["relatório", "reunião", "entrega", "prazo", "financeiro"]

#Classificando a categoria do email
def classify_email(text: str) -> str:
    processed_text = preprocess_text(text)
    prompt = (
        f"Classifique o seguinte email como 'Produtivo' ou 'Improdutivo'. "
        f"Responda apenas com a categoria.\nEmail: {processed_text}"
    )

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    category = response.text.strip()

    match = re.search(r"(Produtivo|Improdutivo)", category, re.IGNORECASE)
    if match:
        return match.group(1).capitalize()
    
    return "Produtivo" if any(word.lower() in text.lower() for word in keywords_produtivo) else "Improdutivo"


#Gerandop a resposta baseada na categoria do email
def generate_response(text: str, category: str) -> str:
    if category == "Produtivo":
        prompt = (
            f"Você é um assistente profissional de emails. "
            f"Responda ao seguinte email de forma clara, objetiva e resumida, "
            f"sem repetir o conteúdo do email original. "
            f"Mantenha um tom formal e profissional, destacando pontos importantes, "
            f"e finalize assinando com meu nome (Vitor Martins) e Equipe AutoU.\n\n"
            f"Email:\n{text}"
        )
    else:
        prompt = (
            f"Você é um assistente de emails educado e breve. "
            f"Responda ao seguinte email de forma curta, educada e objetiva, "
            f"resumindo os pontos principais e sem repetir o conteúdo do email original. "
            f"Finalize sempre com meu nome (Vitor Martins) e Equipe AutoU.\n\n"
            f"Email:\n{text}"
        )

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text.strip()

#Chama as funções para classificar a categoria do email e gerar uma resposta
def process_email(text: str) -> dict:
    category = classify_email(text)
    suggested_response = generate_response(text, category)
    return {"email": text, "categoria": category, "resposta": suggested_response}
