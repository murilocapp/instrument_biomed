from igraph import Graph, plot
import matplotlib.pyplot as plt

def criar_grafo(arquivo):
    G = Graph()
    extra = []
    with open(arquivo, 'r') as f:
        for linha in f:
            # Ignorar linhas que começam com "."
            if linha.startswith(".") or linha.startswith("*") or linha.startswith("$"):
                extra.append(linha)
            else:
                componente, *nos, valor = linha.split()
                if componente.startswith("X"):
                    _componente = componente.split('.')[1]
                    G.add_vertex(_componente)
                    for n in nos[:-1]:
                        G.add_edge(n, _componente)
                    G.add_edge(nos[-1], _componente)
                else:
                    G.add_vertex(componente)
                    nIn, nOut = nos[0], nos[-1]  # Usar os primeiros e últimos nós da lista de nós
                    G.add_edge(nIn, componente)
                    G.add_edge(componente, nOut)
                
    G.vs['label'] = extra
    return G

def desenhar_grafo(G):
    # Ajustar o layout do gráfico
    layout = G.layout_auto()

    # Desenhar o grafo
    visual_style = {}
    visual_style["vertex_size"] = 30
    visual_style["vertex_label"] = G.vs["label"]
    visual_style["bbox"] = (800, 800)
    visual_style["margin"] = 50

    plot(G, **visual_style)
    plt.show()

# Exemplo de uso:
grafo = criar_grafo('Circuitos/circuito_eletreto.txt')
desenhar_grafo(grafo)
