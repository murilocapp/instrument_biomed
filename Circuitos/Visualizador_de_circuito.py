import argparse
import networkx as nx
import matplotlib.pyplot as plt

def criar_grafo(arquivo):
    G = nx.Graph()
    with open(arquivo, 'r') as f:
        for linha in f:
            componente, *nos, valor = linha.split()
            no1, no2 = nos[0], nos[-1]  # Usar os primeiros e últimos nós da lista de nós
            G.add_edge(no1, no2, label=f"{componente} {valor}")
    return G

def desenhar_grafo(G):
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Visualizador de circuito')
    parser.add_argument('-circ', '-c', metavar='"[caminho/arquivo.txt]"', required=True, help='Arquivo contendo informações do circuito')
    args = parser.parse_args()

    G = criar_grafo(args.circ)
    desenhar_grafo(G)

if __name__ == "__main__":
    main()
