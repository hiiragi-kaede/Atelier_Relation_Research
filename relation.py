import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint

material_fname="sophie_materials.txt"
materials,category=[],[]
data=[]
material_info={}
with open(material_fname) as f:
    tmp=[i.split(":") for i in f.readlines()]
    materials=[i[0] for i in tmp]
    category=[i[1][:-2].split(",") for i in tmp]
    material_info={materials[i]:category[i] for i in range(len(materials))}

#pprint(material_info)

recipe_fname="sophie_recipes.txt"
synthesis_info={}
with open(recipe_fname) as f:
    while True:
        name=f.readline()[:-2]
        if name=="": break
        
        components=f.readline().split("[")[1][:-2].split(",")
        components=[i.replace("'","").strip() for i in components]
        category=f.readline().split("[")[1][:-2].split(",")
        category=[i.replace("'","").strip() for i in category]
        synthesis_info[name]={"components":components,
                            "category":category}

#pprint(synthesis_info)

all_categories=set()
for k,v in material_info.items():
    for ele in v:
        all_categories.add(ele)
for k,v in synthesis_info.items():
    for ele in v["category"]:
        all_categories.add(ele)

all_categories=sorted(list(all_categories))
#print(all_categories)

category_items={i:[] for i in all_categories}
for k,v in material_info.items():
    for ele in v:
        category_items[ele].append(k)
for k,v in synthesis_info.items():
    for ele in v["category"]:
        category_items[ele].append(k)

#pprint(category_items)

G=nx.DiGraph()

#素材アイテムをグラフに追加(cyanの点)
for i in range(len(materials)):
    G.add_node(materials[i],color="c")

#調合アイテムをグラフに追加(blueの点)
for k in synthesis_info.keys():
    G.add_node(k,color="b")

pos=nx.spring_layout(G,k=0.4)
node_colors=[node["color"] for node in G.nodes.values()]
nx.draw_networkx_nodes(G,pos,node_color=node_colors,alpha=0.6)
nx.draw_networkx_labels(G,pos,font_size=7,font_family='Yu Gothic',font_weight="bold")

plt.show()