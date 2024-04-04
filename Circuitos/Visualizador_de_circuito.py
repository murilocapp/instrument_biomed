import argparse
import random
from typing import Mapping
import networkx as nx
import matplotlib.pyplot as plt
import PIL
from os import path


def create_icons() -> dict[str, str]:
    icons = {
        'AmpOp': path.join('icons', 'AmpOp.png'),
        'R' : path.join('icons', 'Resistencia.png'),
        'L' : path.join('icons', 'Indutor.png'),
        'C' : path.join('icons', 'Capacitor.png'),
        'V' : path.join('icons', 'FonteTensao.png'),
        'Arduino': path.join('icons', 'Arduino.png'),
        'node': path.join('icons', 'node.webp'),
    }

    images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

    return images

class Grafo(nx.Graph):
    def __init__(self, arquivo):
        self.G = nx.Graph()
        self.arquivo = arquivo
    
    def criar_grafo_simples(self) -> nx.Graph:
        self.extra = []
        with open(self.arquivo, 'r') as f:
            for linha in f:
                if linha.startswith(".") or linha.startswith("*") or linha.startswith("$"):
                    self.extra.append(linha)
                else:
                    componente, *nos, valor = linha.split()
                    if componente.startswith("X"):
                        _componente = componente.split('.')[1]
                        self.G.add_node(_componente)
                        for n in nos[:-1]:
                            self.G.add_node(n)
                            self.G.add_edge(n, _componente)
                        self.G.add_node(nos[-1])
                        self.G.add_edge(_componente, nos[-1])
                    else:
                        self.G.add_node(componente)
                        nIn, nOut = nos[0], nos[-1]  
                        self.G.add_edge(nIn, componente)
                        self.G.add_edge(componente, nOut)
                
        return self.G

    def criar_grafo_complexo(self) -> nx.Graph:
        extra = []
        icons = create_icons()
        comp_nodes = []
        with open(self.arquivo, 'r') as f:
            for linha in f:
                if linha.startswith(".") or linha.startswith("*") or linha.startswith("$"):
                    extra.append(linha)
                else:
                    componente, *nos, valor = linha.split()
                    if componente.startswith("X"):
                        _componente = componente.split('.')[1]
                        self.G.add_node(_componente,image=icons[_componente.split(sep="_")[0]], label=valor)
                        comp_nodes.append(_componente)
                        for n in nos[:-1]:  
                            self.G.add_node(n, name= n, image=icons['node'])
                            self.G.add_edge(n, _componente)
                        self.G.add_node(nos[-1], name = nos[-1] , image=icons['node'])
                        self.G.add_edge(_componente, nos[-1])
                    else:
                        self.G.add_node(componente, image=icons.get(componente[0]), label=valor)
                        comp_nodes.append(componente)
                        nIn, nOut = nos[0], nos[-1]  
                        self.G.add_node(nIn, name = nIn, image=icons['node'])
                        self.G.add_node(nOut, name = nOut, image=icons['node'])
                        self.G.add_edge(nIn, componente)
                        self.G.add_edge(componente, nOut)
        self.extra = extra
        self.comp_nodes = comp_nodes
        return self.G

class Draw:
    def __init__(self):
        pass
    
    @staticmethod
    def desenhar_grafo_complexo(G: nx.Graph):
        # Define o layout com o nó '0' no centro
        seed = 63502528
        k = 1.0 / (1e3) ** 0.5
        pos = nx.spring_layout(G, seed=seed, k=k)

        # Encontrar as coordenadas médias de todos os nós
        x_values = [pos[node][0] for node in G.nodes()]
        y_values = [pos[node][1] for node in G.nodes()]
        x_center = sum(x_values)*5e15 / (len(G.nodes())) 
        y_center = sum(y_values)*5e15 / (len(G.nodes()))

        # Ajustar todas as posições dos nós subtraindo as coordenadas do centro
        pos = {node: (x-x_center, y-y_center) for node, (x, y) in pos.items()}
        fig, ax = plt.subplots()
        #configurar titulo com a seed
        plt.title(f"x_center {x_center}  y_center {y_center}")
        # Note: the min_source/target_margin kwargs only work with FancyArrowPatch objects.
        # Force the use of FancyArrowPatch for edge drawing by setting `arrows=True`,
        # but suppress arrowheads with `arrowstyle="-"`
        nx.draw_networkx_edges(
            G,
            pos=pos,
            ax=ax,
            arrows=True,
            arrowstyle="-",
            connectionstyle="arc3",
            min_source_margin=0.5,
            min_target_margin=0.5,
        )

        # Transform from data coordinates (scaled between xlim and ylim) to display coordinates
        tr_figure = ax.transData.transform
        # Transform from display to figure coordinates
        tr_axes = fig.transFigure.inverted().transform

        # Select the size of the image (relative to the X axis)
        icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.025
        icon_center = icon_size / 2.0

        # Add the respective image to each node
        for n in G.nodes:
            if "image" in G.nodes[n]:
                xf, yf = tr_figure(pos[n])
                xa, ya = tr_axes((xf, yf))
                # get overlapped axes and plot icon
                a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
                a.imshow(G.nodes[n]["image"])
                a.axis("off")
            if "label" in G.nodes[n]:
                plt.text(pos[n][0], pos[n][1], G.nodes[n]["label"], fontsize=6)
            if "name" in G.nodes[n]:
                plt.text(pos[n][0], pos[n][1], G.nodes[n]["name"], fontsize=6)

        plt.show()

@staticmethod
def main():
    parser = argparse.ArgumentParser(description='Visualizador de circuito')
    parser.add_argument('-circ', '-c', metavar='"[caminho/arquivo.txt]"', required=True, help='Arquivo contendo informações do circuito')
    args = parser.parse_args()

    G = Grafo(args.circ)
    G = G.criar_grafo_complexo()
    Draw.desenhar_grafo_complexo(G)


if __name__ == "__main__":
    main()
