from interface import Interface
from scanline import preencher_poligono
from draw import desenhar_pixels
from tkinter import messagebox

# Função de callback chamada ao clicar no botão "Fechar e Preencher"
def executar_preenchimento(pontos, canvas, cor):
    try:
        # Aplica o algoritmo Scanline para obter os segmentos de preenchimento
        segmentos = preencher_poligono(pontos)
        # Desenha os segmentos preenchidos no canvas
        desenhar_pixels(canvas, segmentos, cor=cor)
        return segmentos
    except Exception as erro:
        # Mostra mensagem de erro em caso de falha
        messagebox.showerror('Erro no Preenchimento', f'Ocorreu um erro inesperado:\n{erro}')
        return []

# Função principal do programa
def main():
    # Inicializa a interface gráfica, passando a função de preenchimento como callback
    app = Interface(callback_preencher=executar_preenchimento)
    app.iniciar()

# Garante que o main() seja executado apenas se o script for rodado diretamente
if __name__ == '__main__':
    main()
