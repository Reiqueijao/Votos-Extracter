import json
import os

opcoes = ["a", "b", "c", "d", "e","f"]

# Diretório onde as frases serão salvas
DIRETORIO = "Frases"
ARQUIVO_JSON = os.path.join(DIRETORIO, "Frases.json")

# Garante que o diretório existe
os.makedirs(DIRETORIO, exist_ok=True)

def carregar_frases():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_frases(data):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def adicionar_frase():
    frase = input("Digite sua frase: ")
    autor = input("Nome do autor: ")
    keyword = input("Digite a palavra-chave da frase: ").strip().lower()
    
    data = carregar_frases()
    if keyword not in data:
        data[keyword] = {}
    
    letras_usadas = set(data[keyword].keys())
    letras_disponiveis = [letra for letra in opcoes if letra not in letras_usadas]
    if not letras_disponiveis:
        print(f"A palavra-chave '{keyword}' já tem "+opcoes.__len__().__str__()+" frases registradas.")
        if input("Mais uma? (y/n) ").strip().lower() == 'y':
            adicionar_frase()
        else:
            return

    opcao = letras_disponiveis[0]
    data[keyword][opcao] = {"frase": frase, "autor": autor}
    salvar_frases(data)
    print(f"Frase salva! Palavra-chave: {keyword}, Opção: {opcao}")

    if input("Mais uma? (y/n) ").strip().lower() == 'y':
        adicionar_frase()

adicionar_frase()
