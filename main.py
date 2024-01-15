import tkinter as tk
import keyboard # detectar eventos do teclado
import pyautogui
from extract_text import ExtractText
from show_translate import showImage


# Variáveis globais para armazenar os valores de box e font_size
global_box = None
global_font_size = None

current_language = 'eng'
target_language = 'pt'

# Lista para armazenar as janelas secundárias
# secondary_windows = []

# Criando a janela principal
root = tk.Tk()
root.title("Translate Text By Image")

# componente de texto para exibir o texto extraido
text_display = tk.Text(root, wrap="word", width=40, height=10)
text_display.pack(pady=10)

# botão de retradução
def retraduzir():
    # Obtendo o texto traduzido do widget tk.Text
    texto_traduzido = text_display.get(1.0, tk.END)
    # Atualizando o componente de texto com o novo texto traduzido
    if len(texto_traduzido) >= 1:
        showImage(global_box, texto_traduzido, global_font_size)

# botão de retradução
botao_retraduzir = tk.Button(root, text="Re-translate", command=retraduzir)
botao_retraduzir.pack()

# Definindo a função que seleciona e salva a área da tela
def select_area(Root):
    global global_box, global_font_size  # Declarando as variáveis globais

    # Escondendo a janela principal
    Root.withdraw()
    # Criando uma nova janela transparente que cobre toda a tela
    window = tk.Toplevel(Root)
    window.attributes("-fullscreen", True) # tela inteixa
    window.attributes("-alpha", 0.25) # opacidade de 25%
    window.attributes("-topmost", True) # mantendo a janela no topo de todas as outras
    window.configure(background="grey") # cor cinza

    # Criando um canvas para desenhar o outline
    canvas = tk.Canvas(window, 
                       width=window.winfo_screenwidth(), # altura da janela = resolução width
                       height=window.winfo_screenheight(), # largura da janela = resolução height
                       highlightthickness=0) # sem borda / contorno
    canvas.pack()
    # Definindo as variáveis que armazenam as coordenadas da área selecionada
    x1 = y1 = x2 = y2 = 0
    # Definindo a função que é chamada quando o botão do mouse é pressionado
    def on_click(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
    # Definindo a função que é chamada quando o mouse é movido
    def on_move(event):
        nonlocal x2, y2, canvas
        x2, y2 = event.x, event.y
        # Apagando o outline anterior
        canvas.delete("outline") # atualizando o canvas
        # Desenhando o novo outline
        canvas.create_rectangle(x1, y1, x2, y2,
                                outline="green", # cor verde
                                width=3, # espessura de 3pixels
                                tag="outline") # com contorno
    # Definindo a função que é chamada quando o botão do mouse é solto
    def on_release(event):
        nonlocal x2, y2, window, Root, canvas
        global global_box, global_font_size  # usando as variáveis globais

        x2, y2 = event.x, event.y
        # Fechando a janela transparente
        window.destroy()
        # Verificando se as coordenadas são diferentes de zero
        if x2 != 0 and y2 != 0 and y1 != 0 and x1 != 0:
            image = pyautogui.screenshot() # print da tela inteira

            # Definindo o retângulo para cortar
            box = (x1, y1, x2, y2) # box usado localmente
            global_box = box # global box usando globalmente

            # Cortando a imagem conforme as coordenadas
            img_cortada = image.crop(box)

            # ImageShow.show(img_cortada) # comando de debug

            # Mostrando a janela principal
            Root.deiconify()
            # Extraindo o texto da imagem cortada e o tamanho da fonte
            output_text, font_size = ExtractText(img_cortada, current_language)
            global_font_size = font_size

            text_display.delete(1.0, tk.END) # Limpa o texto anterior
            text_display.insert(tk.END, output_text) # Insere o texto extraido

            # Chama a função showImage para traduzir e mostrar o texto nas coordenadas do box
            showImage(box, output_text, font_size, current_language, target_language)


    # Vinculando os eventos do mouse às funções
    window.bind("<ButtonPress-1>", on_click) # click esquerdo do mouse
    window.bind("<B1-Motion>", on_move) # movimento do mouse esquerdo
    window.bind("<ButtonRelease-1>", on_release) # soltando o click do mouse esquerdo

# É chamada quando tecla de atalho pressionada
def on_key_press():
    # Chamando a função select_area, quando atalho pressionado
    select_area(root)


# configurar o atalho com base nas opções escolhidas
def set_shortcut(value):
    atalho = f"{comando_especial_var.get()}+{tecla_var.get()}"
    keyboard.remove_hotkey(on_key_press) # limpar ultimo atalho
    keyboard.add_hotkey(atalho, on_key_press) # inserir novo atlaho
    label_atalho.config(text=f"Current Shortcut: {atalho}")
    return value

# Criando variáveis para as opções de comando especial e tecla
comandos_especiais = ["CTRL", "SHIFT", "ALT"]
teclas = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "N", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "Z"]
comando_especial_var = tk.StringVar(value="SHIFT")
tecla_var = tk.StringVar(value="F")

# Área 2 (div 2) - Menus de Comando Especial e Tecla
frame_div2 = tk.Frame(root)
frame_div2.pack(pady=5)

label_comando_especial = tk.Label(frame_div2, text="Special Command:")
label_comando_especial.grid(row=0, column=0, padx=5, pady=5, sticky="e")

menu_comando_especial = tk.OptionMenu(frame_div2,
                                      comando_especial_var,
                                      *comandos_especiais,
                                      command=set_shortcut
                                    )
menu_comando_especial.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_tecla = tk.Label(frame_div2, text="Key:")
label_tecla.grid(row=0, column=2, padx=5, pady=5, sticky="e")

menu_tecla = tk.OptionMenu(frame_div2,
                           tecla_var,
                           *teclas,
                            command=set_shortcut)
menu_tecla.grid(row=0, column=3, padx=5, pady=5, sticky="w")


label_atalho = tk.Label(frame_div2, text="Current Shortcut:")
label_atalho.grid(row=2, column=0, columnspan=4, pady=5)

# Adicionando o atalho padrão
key_saved = 'SHIFT+F'
keyboard.add_hotkey(key_saved, on_key_press)
label_atalho.config(text=f"Current Shortcut: {key_saved}")


# Função para traduzir de uma língua para outra
def traduzir(value):
    global current_language, target_language # variaveis globais
    # Obtenha as linguagens selecionados nos menus
    lingua_origem = lingua_origem_var.get()
    lingua_destino = lingua_destino_var.get()

    # Realize a tradução e exiba o resultado onde for necessário
    resultado_traducao = f"Traduzindo de {lingua_origem} para {lingua_destino}"
    print(resultado_traducao)
    print( f"Traduzindo de {language_codes[lingua_origem]} para {language_codes[lingua_destino]}")

    current_language = language_codes[lingua_origem]
    target_language = language_codes[lingua_destino]
    print(current_language, target_language)
    return value

# Área 3 (div 3) - Tradução de uma língua para outra
frame_div3 = tk.Frame(root)
frame_div3.pack(pady=5)

# Criando códigos de idioma para as línguas mais populares
language_codes = {
    "English": "en",
    "Portuguese": "pt",
    "Japanese": "jpn",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Russian": "ru",
    "Chinese": "zh",
    "Arabic": "ar",
}

# Criando variáveis para as opções de língua de origem e língua de destino
linguas = list(language_codes.keys())
lingua_origem_var = tk.StringVar(value="English")
lingua_destino_var = tk.StringVar(value="Portuguese")

# Criando widgets para a escolha da língua de origem e língua de destino
label_lingua_origem = tk.Label(frame_div3, text="Source Language:")
menu_lingua_origem = tk.OptionMenu(frame_div3, lingua_origem_var, *linguas, command=traduzir)

label_lingua_destino = tk.Label(frame_div3, text="Target Language:")
menu_lingua_destino = tk.OptionMenu(frame_div3, lingua_destino_var, *linguas, command=traduzir)

# Posicionando widgets na janela principal
label_lingua_origem.grid(row=0, column=0, padx=5, pady=5)
menu_lingua_origem.grid(row=0, column=1, padx=5, pady=5)
label_lingua_destino.grid(row=0, column=2, padx=5, pady=5)
menu_lingua_destino.grid(row=0, column=3, padx=5, pady=5)

root.mainloop()
