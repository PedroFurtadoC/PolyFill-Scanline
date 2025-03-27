# main.py

from interface import Interface
from scanline import preencher_poligono
from draw import desenhar_pixels
from tkinter import messagebox

def executar_preenchimento(pontos, canvas, cor):
    try:
        segmentos = preencher_poligono(pontos)
        desenhar_pixels(canvas, segmentos, cor=cor)
        return segmentos
    except Exception as erro:
        messagebox.showerror('Erro no Preenchimento', f'Ocorreu um erro inesperado:\n{erro}')
        return []

def main():
    app = Interface(callback_preencher=executar_preenchimento)
    app.iniciar()

if __name__ == '__main__':
    main()
