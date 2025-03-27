# draw.py

def desenhar_linha(x1, y1, x2, y2, canvas, cor='black', largura=2):
    return canvas.create_line(x1, y1, x2, y2, fill=cor, width=largura)

def desenhar_ponto_visual(canvas, x, y, cor='black', raio=3):
    canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill=cor, outline=cor)

def desenhar_poligono(canvas, pontos, cor_linha='black', largura=2):
    for i in range(len(pontos)):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % len(pontos)]
        desenhar_linha(x1, y1, x2, y2, canvas, cor=cor_linha, largura=largura)

def desenhar_pixels(canvas, segmentos, cor='blue'):
    ids = []
    for x_ini, x_fim, y in segmentos:
        linha_id = canvas.create_line(x_ini, y, x_fim, y, fill=cor)
        ids.append(linha_id)
    return ids
