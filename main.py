import json
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

# u = 1 frase faltante
# i = 2 frase faltante
# i = 3 frase faltante
# p = 4 frase faltante

# Diretórios corretos
DIRETORIO_RAW = "RawData"
DIRETORIO_REFINED = "RefinedData"
DIRETORIO_FRASES = "Frases"
ARQUIVO_VOTOS = os.path.join(DIRETORIO_REFINED, "Palavras.json")
ARQUIVO_FRASES = os.path.join(DIRETORIO_FRASES, "Frases.json")

# Garante que os diretórios existem
os.makedirs(DIRETORIO_RAW, exist_ok=True)
os.makedirs(DIRETORIO_REFINED, exist_ok=True)
os.makedirs(DIRETORIO_FRASES, exist_ok=True)

def carregar_votos():
    try:
        with open(ARQUIVO_VOTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"messages": []}

def carregar_frases():
    try:
        with open(ARQUIVO_FRASES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def processar_votos(votos, frases):
    pontuacao = {}
    votos_por_usuario = {}

    
    for mensagem in votos["messages"]:
        conteudo = mensagem["content"].strip().lower()
        autor_id = mensagem["author"]["id"]
        
        if conteudo.startswith("[") and conteudo.endswith("]"):
            partes = conteudo[1:-1].split()
            if len(partes) == 2:
                palavra_chave, ordem_votos = partes
                if palavra_chave in frases and len(ordem_votos) == len(frases[palavra_chave]):
                    if autor_id not in votos_por_usuario:
                        votos_por_usuario[autor_id] = []
                    votos_por_usuario[autor_id].append((palavra_chave, ordem_votos+"z"))
                elif palavra_chave in frases and len(ordem_votos) > len(frases[palavra_chave]):
                    if autor_id not in votos_por_usuario:
                        votos_por_usuario[autor_id] = []
                    print(len(frases[palavra_chave]) - 6)
                    if len(frases[palavra_chave]) - 6 == -1:
                        votos_por_usuario[autor_id].append((palavra_chave, ordem_votos[len(frases[palavra_chave])-len(ordem_votos)-1:len(ordem_votos)-1]+"u"))
                    elif len(frases[palavra_chave]) - 6 == -2:
                        votos_por_usuario[autor_id].append((palavra_chave, ordem_votos[len(frases[palavra_chave])-len(ordem_votos)-1:len(ordem_votos)-1]+"i"))
                    elif len(frases[palavra_chave]) - 6 == -3:
                        votos_por_usuario[autor_id].append((palavra_chave, ordem_votos[len(frases[palavra_chave])-len(ordem_votos)-1:len(ordem_votos)-1]+"o"))
                    elif len(frases[palavra_chave]) - 6 == -4:
                        votos_por_usuario[autor_id].append((palavra_chave, ordem_votos[len(frases[palavra_chave])-len(ordem_votos)-1:len(ordem_votos)-1]+"p"))
    
    for autor_id, votos in votos_por_usuario.items():
        peso_por_voto = 1.0 / len(votos)
        for palavra_chave, ordem_votos in votos:
            if palavra_chave not in pontuacao:
                pontuacao[palavra_chave] = {}
            
            for i, letra in enumerate(ordem_votos):
                if letra == "u":
                    for i2, letra2 in enumerate(ordem_votos):
                        if letra2 != "u":
                            pontuacao[palavra_chave][letra2] += peso_por_voto * (len(ordem_votos) - i2 ) /6
                elif letra == "i":
                    for i2, letra2 in enumerate(ordem_votos):
                        if letra2 != "i":
                            pontuacao[palavra_chave][letra2] += peso_por_voto * (len(ordem_votos) - i2 ) /6
                elif letra == "o":
                    for i2, letra2 in enumerate(ordem_votos):
                        if letra2 != "o":
                            pontuacao[palavra_chave][letra2] += peso_por_voto * (len(ordem_votos) - i2 ) /6
                elif letra == "p":
                    for i2, letra2 in enumerate(ordem_votos):
                        if letra2 != "i":
                            pontuacao[palavra_chave][letra2] += peso_por_voto * (len(ordem_votos) - i2 ) /6
                elif letra == "z":
                    for i2, letra2 in enumerate(ordem_votos):
                        if letra2 != "z":
                            pontuacao[palavra_chave][letra2] += peso_por_voto * (len(ordem_votos) - i2 ) /6

                if letra != "u" and letra != "i" and letra != "o" and letra != "p" and letra != "z":
                    if letra not in pontuacao[palavra_chave]:
                        pontuacao[palavra_chave][letra] = 0
                    pontuacao[palavra_chave][letra] += peso_por_voto * (len(ordem_votos) - i)
    
    return pontuacao

def gerar_grafico_jogador_mais_votado(pontuacao, frases, eliminados):
    votos_por_jogador = {}
    for palavra_chave, opcoes in pontuacao.items():
        for letra, pontos in opcoes.items():
            if letra in frases[palavra_chave]:
                autor = frases[palavra_chave][letra]["autor"]
                if autor not in votos_por_jogador:
                    votos_por_jogador[autor] = 0
                votos_por_jogador[autor] += pontos
    
    if not votos_por_jogador:
        return
    
    jogadores, pontos = zip(*sorted(votos_por_jogador.items(), key=lambda x: x[1], reverse=True))
    cores = []
    for jogador in jogadores:
        if jogador in eliminados:
            cores.append('red')
        else:
            cores.append('green')
    
    plt.figure(figsize=(10, 5))
    plt.barh(jogadores, pontos, color=cores)
    plt.xlabel("Pontuação Total Recebida")
    plt.ylabel("Jogadores")
    plt.title("Jogadores Mais Votados (Eliminados em vermelho)")
    plt.gca().invert_yaxis()
    plt.show()

def exibir_tabela_classificacao(pontuacao, frases):
    tabela = []
    for palavra_chave, opcoes in pontuacao.items():
        for letra, pontos in opcoes.items():
            if letra in frases[palavra_chave]:
                frase = frases[palavra_chave][letra]["frase"]
                autor = frases[palavra_chave][letra]["autor"]
                tabela.append((palavra_chave, frase, autor, pontos))
    
    df = pd.DataFrame(tabela, columns=["Palavra-chave", "Frase", "Autor", "Pontuação"])
    df = df.sort_values(by="Pontuação", ascending=False)
    limite = int(len(df) * 0.8)
    df_classificados = df.iloc[:limite]
    df_eliminados = df.iloc[limite:]
    
    print("Classificação:")
    print(df_classificados.to_string(index=False))
    
    print("\nEliminados:")
    print(df_eliminados.to_string(index=False))
    
    return df_eliminados["Autor"].tolist()

def main():
    inicio = time.time()
    votos = carregar_votos()
    frases = carregar_frases()
    pontuacao = processar_votos(votos, frases)
    eliminados = exibir_tabela_classificacao(pontuacao, frases)
    fim = time.time()
    print(f"Processamento concluído em {fim - inicio:.2f} segundos.")
    gerar_grafico_jogador_mais_votado(pontuacao, frases, eliminados)
    if input("reset das frases? y/n ") == "y":
        with open(ARQUIVO_FRASES, "w", encoding="utf-8") as f:
            json.dump({}, f)

if __name__ == "__main__":
    main()
