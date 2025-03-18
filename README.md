Este projeto processa votos para um jogo no estilo Ten Words of Wisdom (TWOW), organizando frases enviadas pelos jogadores e atribuindo pontos com base nas votações. Ele utiliza o Discord Chat Exporter para extrair mensagens do Discord e analisar os votos. Principais funcionalidades:

✅ Processamento de votos a partir de dados JSON exportados pelo Discord Chat Exporter.
✅ Sistema flexível de frases, permitindo qualquer número de opções.
✅ Classificação de jogadores, destacando os eliminados.
✅ Gráficos visuais para análise dos resultados.
✅ Otimizações de desempenho e suporte a múltiplas palavras-chave.

🔧 Como Usar:
1️⃣ Insira as frases dos jogadores utilizando frases.py. Isso gerará o arquivo Frases.json.
2️⃣ Exporte as mensagens do Discord usando o Discord Chat Exporter e salve o arquivo JSON na pasta RawData/.
3️⃣ Execute refiner.py para limpar e preparar os dados de votação.
4️⃣ Execute main.py para processar os votos, gerar classificações e exibir os resultados.
5️⃣ Visualize as classificações e gráficos para analisar o desempenho dos jogadores.

🚀 Se encontrar bugs ou quiser contribuir, sinta-se à vontade para abrir um pull request.
