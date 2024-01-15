# Importando a biblioteca tkinter
import tkinter as tk
from translate import Translate

def showImage(box, text_extracted, font_size, current_language, target_language):
    # Janela principal
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal

    # Criando a janela que exibe o texto
    window = tk.Toplevel(root)
    window.overrideredirect(True) # removendo as bordas da janela
    window.attributes("-topmost", True) # mantendo a janela no topo de todas as outras

    # Definindo o texto a ser exibido
    translated_text = Translate(text_extracted, current_language, target_language)
    # Label que exibe o texto
    label = tk.Label(window,
        text=translated_text,
        font=("Times New Roman", font_size, 'bold'),
        bg="white")
    label.pack()

    # Função que fecha a janela ao ser clicada
    def on_click(event):
        root.destroy() # Fechando a janela
        return event

    # Definindo as coordenadas da janela
    x1 = int(box[0]) # coordenada x da esquerda da área
    y2 = int(box[1]) # coordenada y do fundo da área
    x2 = int(box[2]) # coordenada x da direita da área
    y1 = int(box[3]) # coordenada y do topo da área

    w = label.winfo_reqwidth() # largura do texto
    h = label.winfo_reqheight() # altura do texto

    # Ajuste das coordenadas para que o texto fique dentro da área
    x = (x1 + x2) / 2 - w / 2 # coordenada x do centro do texto
    y = (y1 + y2) / 2 - h / 2 # coordenada y do centro do texto

    # Arredondando os valores de x e y para números inteiros
    x = round(x)
    y = round(y)

    # Posicionando a janela de acordo com as coordenadas
    window.geometry(f"{w}x{h}+{x}+{y}")

    # Vinculando o evento de clique da janela a função
    window.bind("<Button-1>", on_click)

    root.mainloop()
    return window