import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint

fname="sophie_materials.txt"
materials,category=[],[]
data=[]
with open(fname) as f:
    tmp=[i.split(":") for i in f.readlines()]
    data=[[i[0],i[1][:-2]] for i in tmp]
    materials=[i[0] for i in tmp]
    category=[i[1][:-2].split(",") for i in tmp]
    
G=nx.DiGraph()

for i in range(len(materials)):
    G.add_node(materials[i],color="c")

pos=nx.spring_layout(G,k=0.4)
node_colors=[node["color"] for node in G.nodes.values()]
nx.draw_networkx_nodes(G,pos,node_color=node_colors,alpha=0.6)
nx.draw_networkx_labels(G,pos,font_size=7,font_family='Yu Gothic',font_weight="bold")

plt.show()