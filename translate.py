import requests


def remove_newlines(texto):
    text_clean = texto.replace('\n', ' ► ') # Substitui a quebra linha por um caracter especial com espaço
    # Separa o texto em array
    arr = text_clean.split()
    # salva a ordem (position) do caracter especial em um array
    positions = []
    for index in range(len(arr)):
        if arr[index] == "►":
            positions.append(index)
    # retorna as posições e o texto limpo
    return positions, texto.replace('\n', ' ')

def adding_newlines(texto, positions):
    texto_splited = texto.split() # Separa o texto e armazenar em um array
    # remover espaçamento adjascentes, evitando quebra de linhas proximas
    if len(positions) >= 2: # Mais de 1 posição?
        # Verifica se as posições iniciais são adjascentes
        if positions[0] == positions[1]:
            positions.pop(1)

        i = len(positions) - 2
        while i > 0:
            # Verifica e remove textos adjascentes
            if positions[i] == positions[i-1] + 1 or positions[i] == positions[i+1] - 1:
                positions.pop(i)
            i -= 1

    # Inserir espaçamento (positions)
    for i in positions:
        texto_splited.insert(i, "\n")

    return " ".join(texto_splited)


def Translate(text, current_language, target_language):
    # Anota as posições da quebra linha e retorna um texto limpo
    positions, cleaned_text = remove_newlines(text)

    if current_language =='jpn':
        current_language = 'ja'

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': current_language,
        'tl': target_language,
        'dt': 't',
        'q': cleaned_text,
    }
    response = requests.get(url, params=params, timeout=15)

    translation_data = response.json()

    # Processa a resposta para obter o texto completo
    translated_text = ''.join(part[0] for part in translation_data[0])

    # Adiciona as quebras de linha \n de volta, com base nas quebras de linha \n originais
    translated_text_with_newlines = adding_newlines( translated_text, positions )
    print('Original:\n', cleaned_text)
    print('................')
    print('Tradução:\n', translated_text_with_newlines)

    return translated_text_with_newlines.strip()


