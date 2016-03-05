import requests
import urllib2
import bz2
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import os.path

br = set()
us = set()

with open("br.as", 'rb') as f:
    for line in f:
        br.add(line.strip())

with open("us.as", 'rb') as f:
    for line in f:
        us.add(line.strip())


filename = 'temp.file'  

if not os.path.isfile(filename):
    
    print "downloading dataset"
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
else:
    print "using existing dataset"

print "gathering intersections and building graph"
G=nx.Graph()

# Turns out adding nodes that aren't used kills memory.
'''
print "adding nodes"
for node in br|us:
    G.add_node(node)
'''

br_used = set()
us_used = set()
NO_used = set()

print "adding edges"
with open(filename, 'rb') as f:
    for line in f:
        temp = line.split()[6:-1]

        # sets of important ASes in line
        tbr = set(temp)&br
        tus = set(temp)&us


        ### TODO: US NETWORK     ###

        ### TODO: BRAZIL NETWORK ###

        ### BRAZIL TO US ROUTES  ###

	if len(tbr) > 0 and len(tus) > 0: #For lines that have both a BR-AS and a US-AS add edges between those ASes
            # left trim non brazil and US ASes
            for t in temp:
                if t in tbr|tus:
                    break
                temp = temp[1:]

            # right trim non brazil and US ASes
            for t in temp[::-1]:
                if t in tbr|tus:
                    break
                temp = temp[:-1]

	    for x in tbr:   
                for y in tus:
                    br_used.add(int(x))
                    us_used.add(int(y))
            AS_TEMP = None
            for AS in temp:
                try:
                    G.add_node(int(AS))
                    if AS not in tbr and AS not in tus:
                        NO_used.add(int(AS))
                    try:
                        G.add_edge(int(AS_TEMP),int(AS))
                    except TypeError as e:
                        AS = AS
                    AS_TEMP = AS
                except ValueError as e:
                    continue

print "brazil nodes:",len(br_used)
print "us nodes:    ",len(us_used)
print "other nodes: ",len(NO_used)
print "edges:       ",len(G.edges())


print "setting positions"
pos = nx.spring_layout( G ) #This consumes memory. This line tries to set the positions of all of the Nodes and edges in the map

print "drawing brazil nodes"
nx.draw_networkx_nodes(G,pos,
                       nodelist=br_used,
                       node_color='r',  #We need to make the brazil and US nodes seperate colors
                       node_size=40,
                       node_shape='o',
                   alpha=0.8)

print "drawing us nodes"
nx.draw_networkx_nodes(G,pos,
                       nodelist=us_used,
                       node_color='b', #US is blue
                       node_size=40,
                       node_shape='s',
                   alpha=0.8)

print "drawing none nodes"
nx.draw_networkx_nodes(G,pos,
                       nodelist=NO_used,
                       node_color='g',  #We need to make the brazil and US nodes seperate colors
                       node_size=40,
                       node_shape='^',
                   alpha=0.8)

print "drawing edges"
nx.draw_networkx_edges(G,pos)

_xlim = plt.gca().get_xlim() # grab the xlims
_ylim = plt.gca().get_ylim() # grab the ylims

print "showing graph"
plt.show()
