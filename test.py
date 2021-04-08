import graphviz as gpz

g = gpz.Graph("Set_Build_Process")

g.node('v1', color="gray45", style="filled", label="{1}")
g.node('v2', color="gray45", style="filled", label="{1,2}")
g.node('v3', color="gray45", style="filled", label="{1,3}")
g.node('v4', color="gray45", style="filled", label="{1,4,3}")
g.node('v5', color="gray45", style="filled", label="{3,5}")
g.node('v6', color="gray45", style="filled", label="{4,6}")
g.node('v7', color="gray45", style="filled", label="{4,7}")

g.edge('v1', 'v2')
g.edge('v1', 'v3')
g.edge('v1', 'v4')
g.edge('v3', 'v5')
g.edge('v3', 'v4')
g.edge('v4', 'v6')
g.edge('v4', 'v7')



g.render("Set_Build_Process7.gv", view=True)
