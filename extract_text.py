import pytesseract

# Definir o caminho do executável do tesseract
# site : https://tesseract-ocr.github.io/tessdoc/Downloads.html
# download link: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe
pytesseract.pytesseract.tesseract_cmd = r"tesseract.exe" # exemplo D:\Python\Tesseract-OCR\tesseract.exe

font_default = 18

def ExtractText(img, current_language):
    img_cinza = img.convert("L")
    regioes_texto = pytesseract.image_to_boxes(img_cinza)

    # Itera sobre as regiões de texto
    font_count = 0
    font_size = 0
    for regiao in regioes_texto.splitlines():
        regiao = regiao.split()
        tamanho_fonte = abs(int(regiao[4]) - int(regiao[2]))
        font_count = font_count + 1
        font_size+= tamanho_fonte

    # Calcula a média dos tamanhos de fonte
    if font_size > 0:
        font_size = int(font_size / font_count)
    else:
        font_size = font_default

    # Extrair o texto
    ########################## psm3 ou psm5 (psm 5 é pra textos vertical)
    text = pytesseract.image_to_string(img_cinza, current_language, config='--psm 3')
    text = text.strip()

    # Retornar se nao conseguir extrair o texto
    if len(text) <= 0:
        print('erro, texo vazio retornando')
        return
    return text, font_size
