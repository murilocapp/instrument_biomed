import argparse
import networkx as nx
import matplotlib.pyplot as plt
import PIL
from os import path


def create_icons()-> dict[str,str]:
        icons = {
            'AmpOp': path('icons', 'AmpOp.png'),
            'R' : path('icons', 'Resistencia.png'),
            'L' : path('icons', 'Indutor.png'),
            'C' : path('icons', 'Capacitor.png'),
            'V' : path('icons', 'FonteTensao.png'),
            'Arduino': path('icons', 'Arduino.png'),
        }

        images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

        return images


class Grafo(nx.Graph):
    def __init__(self,arquivo):
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
                    if(componente.startswith("X")):
                        _componente = componente.split('.')[1]
                        self.G.add_node(_componente)
                        for n in nos[:-1]:
                            self.G.add_node(n)
                            self.G.add_edge(n, _componente)
                        self.G.add_node(nos[-1])
                        self.G.add_edge(_componente,nos[-1])
                    else:
                        self.G.add_node(componente)
                        nIn, nOut = nos[0], nos[-1]  # Usar os primeiros e últimos nós da lista de nós
                        self.G.add_edge(nIn, componente)
                        self.G.add_edge(componente, nOut)
                
        return self.G

    def criar_grafo_complexo(self) -> nx.Graph:
        extra = []
        icons = create_icons()
        with open(self.arquivo, 'r') as f:
            for linha in f:
                if linha.startswith(".") or linha.startswith("*") or linha.startswith("$"):
                    extra.append(linha)
                else:
                    componente, *nos, valor = linha.split()
                    if(componente.startswith("X")):
                        _componente = componente.split('.')[1]
                        self.G.add_node(_componente, image = icons[_componente.split(sep="_")[0]], label = valor)
                        for n in nos[:-1]:  
                            self.G.add_edge(n, _componente)
                        self.G.add_edge(_componente, nos[-1])
                    else:
                        self.G.add_node(componente, image = icons[componente[0]],label = valor)
                        nIn, nOut = nos[0], nos[-1]  
                        self.G.add_edge(nIn, componente)
                        self.G.add_edge(componente, nOut)
        self.extra = extra
        return self.G



class Draw:
    def __init__(self):
        pass
    
    @staticmethod  # Decorador para tornar a função estática (não precisa instanciar a classe)
    def desenhar_grafo(G:nx.Graph):
        pos = nx.spring_layout(G, seed=1734289230)
        fig, ax = plt.subplots()

        # Note: the min_source/target_margin kwargs only work with FancyArrowPatch objects.
        # Force the use of FancyArrowPatch for edge drawing by setting `arrows=True`,
        # but suppress arrowheads with `arrowstyle="-"`
        nx.draw_networkx_edges(
            G,
            pos=pos,
            ax=ax,
            arrows=True,
            arrowstyle="-",
            min_source_margin=15,
            min_target_margin=15,
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
            xf, yf = tr_figure(pos[n])
            xa, ya = tr_axes((xf, yf))
            # get overlapped axes and plot icon
            a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
            a.imshow(G.nodes[n]["image"])
            a.axis("off")
        plt.show()



#-----------------------------------------------------------------------------------------------------------

@staticmethod
def main():
    parser = argparse.ArgumentParser(description='Visualizador de circuito')
    parser.add_argument('-circ', '-c', metavar='"[caminho/arquivo.txt]"', required=True, help='Arquivo contendo informações do circuito')
    args = parser.parse_args()

    G = Grafo(args.circ)
    G.criar_grafo_simples()
    Draw.desenhar_grafo(G)

if __name__ == "__main__":
    main()