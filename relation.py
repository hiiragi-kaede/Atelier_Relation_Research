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

#レシピのエッジをグラフに追加    
for name in synthesis_info.keys():
    recipe=synthesis_info[name]["components"]
    for material in recipe:
        if "(" in material:
            for cate_item in category_items[material]:
                G.add_edge(cate_item,name,info="錬金:"+name)
                G.add_edge(cate_item,"失敗作の灰",info="失敗:"+name)
        else:
            G.add_edge(material,name,info="錬金:"+name)
            G.add_edge(material,"失敗作の灰",info="失敗:"+name)

#pprint(G.edges(data=True))

pos=nx.spring_layout(G,k=0.8)
pr=nx.pagerank(G)
pr=sorted(pr.items(),key=lambda x:x[1],reverse=True)

plt.figure(figsize=(24,16))
node_colors=[node["color"] for node in G.nodes.values()]

nx.draw_networkx_nodes(G,pos,node_color=node_colors,alpha=0.6)
#ノードの大きさをpagerankで動的に変更するバージョン。失敗作の灰のrankが高すぎるので使いにくいかと
#nx.draw_networkx_nodes(G,pos,node_color=node_colors,alpha=0.6,node_size=[5000*v for v in pr.values()])

nx.draw_networkx_labels(G,pos,font_size=6,font_family='Yu Gothic',font_weight="bold")
nx.draw_networkx_edges(G,pos,edge_color="#377eb8",alpha=0.5)

plt.axis('off')
#plt.savefig("sophie_relation.png")
#plt.show()

fname="sophie_pagerank.txt"
with open(fname,"w") as f:
    for ele in pr:
        print(ele,file=f)

cate_item_key=sorted(category_items.items(),key=lambda x:len(x[1]),reverse=True)
fname="sophie_category_size.txt"
with open(fname,"w") as f:
    for k,v in cate_item_key:
        print(str(k)+"  size:"+str(len(v)),file=f)

print("node size:",len(G.nodes()))
print("edge size:",len(G.edges()))