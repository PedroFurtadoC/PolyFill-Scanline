# interface.py

from tkinter import Tk, Canvas, Button, messagebox, colorchooser, Label, Frame
from draw import desenhar_linha, desenhar_ponto_visual
import time

class Interface:
    def __init__(self, callback_preencher=None):
        self.janela = Tk()
        self.janela.title('📐 PolyFill Scanline')

        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        self.largura = int(largura_tela * 0.9)
        self.altura = int(altura_tela * 0.9)
        self.janela.geometry(f"{self.largura}x{self.altura}+50+50")

        self.callback_preencher = callback_preencher
        self.pontos = []
        self.linhas_canvas = []
        self.contador_cliques = 0
        self.cor_preenchimento = '#00aaff'
        self.clique_ativo = True

        self.frame_principal = Frame(self.janela)
        self.frame_principal.pack(fill="both", expand=True)

        largura_canvas = int(self.largura * 0.8)
        largura_painel = int(self.largura * 0.2)

        self.canvas = Canvas(self.frame_principal, width=largura_canvas, height=self.altura, bg='#f0f0f0')
        self.canvas.pack(side='left', fill='both', expand=True)

        self.painel = Frame(self.frame_principal, width=largura_painel, bg='#ffffff')
        self.painel.pack(side='right', fill='y')

        Label(self.painel, text="PolyFill Scanline", font=('Helvetica', 16, 'bold'), bg='#ffffff').pack(pady=15)
        Label(self.painel, text="Desenhe um polígono com\nmínimo de 10 pontos.", font=('Helvetica', 10), bg='#ffffff').pack()

        Button(self.painel, text="🎨 Cor do Preenchimento", font=('Helvetica', 11),
               command=self.selecionar_cor).pack(pady=10, fill='x', padx=15)

        Button(self.painel, text="✅ Fechar e Preencher", font=('Helvetica', 11),
               command=self.fechar_e_preencher).pack(pady=10, fill='x', padx=15)

        Button(self.painel, text="🗑️ Limpar Canvas", font=('Helvetica', 11),
               command=self.limpar_canvas).pack(pady=10, fill='x', padx=15)

        Button(self.painel, text="🚪 Encerrar", font=('Helvetica', 11),
               command=self.encerrar_programa).pack(pady=10, fill='x', padx=15)

        self.label_contador = Label(self.painel, text="Cliques: 0 (mínimo 10)", font=('Helvetica', 11, 'bold'), bg='#ffffff')
        self.label_contador.pack(pady=(10, 2))

        self.label_tempo = Label(self.painel, text="", font=('Helvetica', 10), bg='#ffffff', fg='#555555')
        self.label_tempo.pack(pady=(0, 10))

        self.status_bar = Label(self.janela, text="Clique no canvas para começar o polígono.",
                                bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

        self.canvas.bind("<Button-1>", self.capturar_clique)

    def selecionar_cor(self):
        cor = colorchooser.askcolor(title='Escolha a cor')
        if cor[1]:
            self.cor_preenchimento = cor[1]
            self.status_bar.config(text=f"🎨 Cor escolhida: {self.cor_preenchimento}")

    def capturar_clique(self, evento):
        if not self.clique_ativo:
            self.status_bar.config(text="⚠️ Canvas bloqueado! Clique em 'Limpar Canvas' para reiniciar.")
            return

        x, y = evento.x, evento.y
        if x < 0 or y < 0:
            self.status_bar.config(text="❌ Clique inválido.")
            return

        self.pontos.append((x, y))
        self.contador_cliques += 1
        self.label_contador.config(text=f"Cliques: {self.contador_cliques}")
        desenhar_ponto_visual(self.canvas, x, y)

        if len(self.pontos) > 1:
            x1, y1 = self.pontos[-2]
            linha = desenhar_linha(x1, y1, x, y, self.canvas)
            self.linhas_canvas.append(linha)

        self.status_bar.config(text=f"📍 Ponto ({x}, {y}) adicionado.")

    def fechar_e_preencher(self):
        if not self.callback_preencher:
            messagebox.showerror("Erro", "Nenhum callback de preenchimento foi fornecido.")
            return

        if len(self.pontos) < 10:
            messagebox.showwarning("⚠️ Aviso", "É necessário pelo menos 10 pontos.")
            return

        desenhar_linha(self.pontos[-1][0], self.pontos[-1][1], self.pontos[0][0], self.pontos[0][1], self.canvas)

        self.status_bar.config(text="⏳ Processando preenchimento Scanline...")

        try:
            inicio = time.time()
            pixels = self.callback_preencher(self.pontos, self.canvas, self.cor_preenchimento)
            fim = time.time()
            tempo_execucao = fim - inicio
        except Exception as erro:
            messagebox.showerror("Erro de Execução", f"Erro ao preencher o polígono:\n{erro}")
            self.status_bar.config(text="❌ Erro no preenchimento.")
            return

        self.label_tempo.config(text=f"⏱️ Tempo de execução: {tempo_execucao:.3f} s")
        self.status_bar.config(text="✅ Preenchimento concluído com sucesso!")
        self.clique_ativo = False

    def limpar_canvas(self):
        self.canvas.delete('all')
        self.pontos.clear()
        self.linhas_canvas.clear()
        self.contador_cliques = 0
        self.label_contador.config(text="Cliques: 0 (mínimo 10)")
        self.label_tempo.config(text="")
        self.status_bar.config(text="🧹 Canvas limpo. Comece um novo polígono.")
        self.clique_ativo = True

    def encerrar_programa(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja encerrar?"):
            self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()
