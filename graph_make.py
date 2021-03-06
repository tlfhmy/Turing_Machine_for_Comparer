from graphviz import Digraph

g = Digraph("Tree")
g.node(name='1', label="OR")
g.node(name='2', label="OR")
g.node(name='3', label="OR")
g.node(name='4', label="AND")
g.node(name='5', label="x4")
g.node(name='6', label="AND")
g.node(name='7', label="NOT")
g.node(name='8', label="AND")
g.node(name='9', label="x3")
g.node(name='10', label="x5")
g.node(name='11', label="x6")
g.node(name='12', label="x7")
g.node(name='13', label="x1")
g.node(name='14', label="x2")

g.edge('1', '2')
g.edge('1', '3')
g.edge('2', '4')
g.edge('2', '5')
g.edge('3', '6')
g.edge('3', '7')
g.edge('4', '8')
g.edge('4', '9')
g.edge('6', '10')
g.edge('6', '11')
g.edge('7', '12')
g.edge('8', '13')
g.edge('8', '14')

g.render("Tree.gv", view=True)
