def preencher_poligono(pontos):
    # Garante que o polígono tenha pelo menos 3 vértices
    if len(pontos) < 3:
        return []

    segmentos_preenchimento = []

    # Determina os limites verticais do polígono
    ymin = min(y for _, y in pontos)
    ymax = max(y for _, y in pontos)

    # Cria a Tabela de Arestas (ET), agrupando arestas por sua coordenada y inicial
    edge_table = {y: [] for y in range(ymin, ymax + 1)}
    n = len(pontos)

    for i in range(n):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % n]  # Conecta ao próximo vértice, com fechamento automático

        # Ignora arestas horizontais, pois não contribuem com interseções úteis
        if y1 == y2:
            continue

        # Garante que a aresta seja processada de baixo para cima
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        # Calcula o inverso da inclinação (deltaX / deltaY)
        m_inv = (x2 - x1) / (y2 - y1)

        # Adiciona a aresta à edge_table na linha de varredura y1
        edge_table[y1].append({'x': x1, 'm_inv': m_inv, 'ymax': y2})

    active_edges = []

    # Varre da linha mais baixa até a mais alta (Scanline)
    for y in range(ymin, ymax + 1):
        # Adiciona novas arestas que começam nesta linha
        if y in edge_table:
            active_edges.extend(edge_table[y])

        # Remove arestas que já foram totalmente processadas
        active_edges = [e for e in active_edges if e['ymax'] > y]

        # Ordena as arestas ativas pelo valor atual de x
        active_edges.sort(key=lambda e: e['x'])

        # Percorre as arestas aos pares para formar segmentos horizontais
        for i in range(0, len(active_edges), 2):
            if i + 1 >= len(active_edges):
                break
            x_ini = int(round(active_edges[i]['x']))
            x_fim = int(round(active_edges[i + 1]['x']))
            if x_fim >= x_ini:
                # Armazena o segmento horizontal de preenchimento
                segmentos_preenchimento.append((x_ini, x_fim, y))

        # Atualiza o valor de x de cada aresta ativa com base em sua inclinação
        for edge in active_edges:
            edge['x'] += edge['m_inv']

    return segmentos_preenchimento
