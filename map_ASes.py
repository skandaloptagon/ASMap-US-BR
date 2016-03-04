import requests
import urllib2
import bz2
import networkx as nx
import matplotlib.pyplot as plt
import pylab

br = set()
us = set()

with open("br.as", 'rb') as f:
    for line in f:
        br.add(line.strip())

with open("us.as", 'rb') as f:
    for line in f:
        us.add(line.strip())


print "downloading dataset"
filename = 'temp.file'  
req = urllib2.urlopen('http://archive.routeviews.org/oix-route-views/2016.02/oix-full-snapshot-2016-02-01-0200.bz2')
CHUNK = 16 * 1024

print "decrompressing dataset"
decompressor = bz2.BZ2Decompressor()
with open(filename, 'wb') as fp:
    while True:
        chunk = req.read(CHUNK)
        if not chunk:
            break
        fp.write(decompressor.decompress(chunk))
req.close()

print "gathering intersections and building graph"
G=nx.Graph()

print "adding nodes"
for node in br|us:
    G.add_node(node)

print "adding edges"
with open(filename, 'rb') as f:
    for line in f:
        temp = set(line.split())
	if len(temp&br) > 0 and len(temp&us) > 0:
	    for x in temp&br:
                for y in temp&us:
                    G.add_edge(x,y)

print "setting positions"
pos = nx.spring_layout( G )

print "drawing brazil nodes"
nx.draw_networkx_nodes(G,pos,
                       nodelist=br,
                       node_color='r',
                       node_size=50,
                   alpha=0.8)

print "drawing us nodes"
nx.draw_networkx_nodes(G,pos,
                       nodelist=us,
                       node_color='r',
                       node_size=50,
                   alpha=0.8)

print "drawing edges"
nx.draw_networkx_edges(G,pos)

_xlim = plt.gca().get_xlim() # grab the xlims
_ylim = plt.gca().get_ylim() # grab the ylims

print "showing graph"
plt.show()
