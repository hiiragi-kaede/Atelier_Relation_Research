import matplotlib.pyplot as plt
import networkx as nx

#素材情報を取得
material_fname="sophie_materials.txt"
materials,category=[],[]
data=[]
material_info={}
with open(material_fname) as f:
    tmp=[i.split(":") for i in f.readlines()]
    materials=[i[0] for i in tmp]
    category=[i[1][:-2].split(",") for i in tmp]
    material_info={materials[i]:category[i] for i in range(len(materials))}

#調合品情報を取得
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

#素材・調合品のカテゴリを取得し、setで重複を取り除くことで、カテゴリ集合を取得
all_categories=set()
for k,v in material_info.items():
    for ele in v:
        all_categories.add(ele)
for k,v in synthesis_info.items():
    for ele in v["category"]:
        all_categories.add(ele)

all_categories=sorted(list(all_categories))

#そのカテゴリに属するアイテム一覧を作成
category_items={i:[] for i in all_categories}
for k,v in material_info.items():
    for ele in v:
        category_items[ele].append(k)
for k,v in synthesis_info.items():
    for ele in v["category"]:
        category_items[ele].append(k)


def research1():
    """
        カテゴリを要求する素材をすべて各素材からの辺に変換、すなわち各レシピに使える素材全てから調合品への辺を張る方式。
    """    
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

    print("node size:",len(G.nodes()))
    print("edge size:",len(G.edges()))
    pos=nx.spring_layout(G,k=0.8)
    
    #ページランクを求め、重要度順にソート
    pr=nx.pagerank(G)
    pr=sorted(pr.items(),key=lambda x:x[1],reverse=True)

    plt.figure(figsize=(24,16))
    node_colors=[node["color"] for node in G.nodes.values()]

    nx.draw_networkx_nodes(G,pos,node_color=node_colors,alpha=0.6)
    nx.draw_networkx_labels(G,pos,font_size=6,font_family='Yu Gothic',font_weight="bold")
    nx.draw_networkx_edges(G,pos,edge_color="#377eb8",alpha=0.5)

    plt.axis('off')
    plt.savefig("sophie_relation.png")

    fname="sophie_pagerank.txt"
    with open(fname,"w") as f:
        for ele in pr:
            print(ele,file=f)

    cate_item_key=sorted(category_items.items(),key=lambda x:len(x[1]),reverse=True)
    fname="sophie_category_size.txt"
    with open(fname,"w") as f:
        for k,v in cate_item_key:
            print(str(k)+"  size:"+str(len(v)),file=f)

    


def research2():
    """
        カテゴリを点として追加し、各素材やアイテムのカテゴリもその点への辺として管理する方式。
    """    
    #ループ調合などを探すためのグラフの作成
    G=nx.DiGraph()

    #素材アイテムをグラフに追加(cyanの点)
    for i in range(len(materials)):
        G.add_node(materials[i],color="c")

    #調合アイテムをグラフに追加(blueの点)
    for k in synthesis_info.keys():
        G.add_node(k,color="b")

    #カテゴリをグラフに追加(palegreenの点)
    for k in category_items:
        G.add_node(k,color="palegreen")
    
    #各アイテムのカテゴリ情報を辺として追加
    for k in material_info.keys():
        for category in material_info[k]:
            G.add_edge(k,category,info="素材カテゴリ")
    for k in synthesis_info.keys():
        for category in synthesis_info[k]["category"]:
            G.add_edge(k,category,info="調合品カテゴリ")
    
    #レシピを辺として追加
    for name in synthesis_info.keys():
        recipe=synthesis_info[name]["components"]
        for item in recipe:
            G.add_edge(item,name,info="錬金:"+name)
            G.add_edge(item,"失敗作の灰",info="失敗:"+name)
    
    print("node size:",len(G.nodes()))
    print("edge size:",len(G.edges()))
    pos=nx.spring_layout(G,k=0.7)

    plt.figure(figsize=(24,16))
    node_colors=[node["color"] for node in G.nodes.values()]

    nx.draw_networkx_nodes(G,pos,node_color=node_colors,alpha=0.6)
    
    nx.draw_networkx_labels(G,pos,font_size=6,font_family='Yu Gothic',font_weight="bold")
    nx.draw_networkx_edges(G,pos,edge_color="#377eb8",alpha=0.5)

    plt.axis('off')
    plt.savefig("sophie_relation_with_category.png")
    
    pr=nx.pagerank(G)
    pr=sorted(pr.items(),key=lambda x:x[1],reverse=True)
    fname="sophie_pagerank_with_category.txt"
    with open(fname,"w") as f:
        for ele in pr:
            print(ele,file=f)
    
    fname="sophie_important_items.txt"
    with open(fname,"w") as f:
        for ele in pr:
            print(ele[0],":",file=f)
            print("派生元:",list(G.predecessors(ele[0])),file=f)
            print("使いみち:",list(G.successors(ele[0])),file=f)
            print(file=f)

if __name__=="__main__":
    type=int(input("""\
1->カテゴリを点で管理しない
2->カテゴリを点で管理
グラフのタイプを入力:"""))
    if type==1:
        research1()
    elif type==2:
        research2()