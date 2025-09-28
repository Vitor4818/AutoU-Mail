import re
import spacy

#Carrega o modelo de português
nlp = spacy.load("pt_core_news_sm")

def preprocess_text(text: str) -> str:
    """Limpa, normaliza e aplica lemmatização ao texto.
       Remove pontuação, stopwords e mantém apenas palavras alfabéticas."""
    
    #Removendo caracteres especiais e substituindo por espaço para não grudar palavras
    text = re.sub(r"[^\w\s]", " ", text)
    text = text.lower()

    doc = nlp(text)
    
    #Apenas lemas de palavras que não são stopwords e são alfabéticas
    words = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

    return " ".join(words)
