# scanline.py

def preencher_poligono(pontos):
    if len(pontos) < 3:
        return []

    segmentos_preenchimento = []
    ymin = min(y for _, y in pontos)
    ymax = max(y for _, y in pontos)

    edge_table = {y: [] for y in range(ymin, ymax + 1)}
    n = len(pontos)

    for i in range(n):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % n]

        if y1 == y2:
            continue

        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        m_inv = (x2 - x1) / (y2 - y1)
        edge_table[y1].append({'x': x1, 'm_inv': m_inv, 'ymax': y2})

    active_edges = []

    for y in range(ymin, ymax + 1):
        if y in edge_table:
            active_edges.extend(edge_table[y])

        active_edges = [e for e in active_edges if e['ymax'] > y]
        active_edges.sort(key=lambda e: e['x'])

        for i in range(0, len(active_edges), 2):
            if i + 1 >= len(active_edges):
                break
            x_ini = int(round(active_edges[i]['x']))
            x_fim = int(round(active_edges[i + 1]['x']))
            if x_fim >= x_ini:
                segmentos_preenchimento.append((x_ini, x_fim, y))

        for edge in active_edges:
            edge['x'] += edge['m_inv']

    return segmentos_preenchimento
