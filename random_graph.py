import random
import math 
import numpy as np
import sys
np.set_printoptions(linewidth=2000)

X=100
Y=100
n = X+Y

Xv = range(X)
Yv = range(X, X+Y)

# Adjacency Matrix
E = [[0 for j in range(X+Y)] for i in range(X+Y)]

# Read p and e from the command line arguments
p = float(sys.argv[1])
e = float(sys.argv[2])

q = p-e/math.sqrt(n)

# Generate the graph according to the planted partition model for bisections
def generate():
	for i in range(X+Y):	
		for j in range(X+Y):	
			if i >= j: 
				continue		
			rvalue = random.random()
			
			if (i<X and j<X) or (i>=X and j>=X):
				if rvalue < p:
					E[i][j] = 1
			else:
				if rvalue < q:
					E[i][j] = 1
					
			E[j][i] = E[i][j]

# Rename the initial vertices to remove the spatial locality in the adjacency matrix
def shuffle_vert():
	global E
	global Xv
	global Yv
	E2 = [[0 for j in range(X+Y)] for i in range(X+Y)]
	vertices = range(X+Y)
	random.shuffle(vertices)
	for i in range(X+Y):
		for j in range(X+Y):
			E2[i][j] = E[vertices[i]][vertices[j]]
	for i in range(X): Xv[i]=vertices.index(i)
	for i in range(Y): Yv[i]=vertices.index(X+i)
	E=E2	

# Function to export a graph file (gephi format)
def print_graph_file():
	s = ";" + str(range(X+Y)).replace("[","").replace("]","").replace(",",";").replace(" ","")+"\n"
	for i in range(X+Y):
		s+=str(i)+";"
		for j in range(X+Y):
			s+= str(E[i][j]) + ";"
		s+="\n"
	f = open("g.csv","w")
	f.write(s); f.close()

# Function to export a graph file (dot format)
def print_graph_file2():
	s = "graph {\n"
	for i in range(X+Y):
		for j in range(i):
			if E[i][j]==1:
				s+=str(i)+"--"+str(j)+"\n"
	s+="}"
	f = open("g.dot","w")
	f.write(s); f.close()

generate()
#print_graph_file() 
shuffle_vert()

# Calculate all eigenvalues and eigenvectors			
eigx = np.linalg.eig(E)
w, v = eigx[0], eigx[1]

eigenvalues=list(w)
eigenvaluess=sorted(eigenvalues)
w2i=0

# Select the index of the second largest eigenvalue
w2i=eigenvalues.index(eigenvaluess[-2])

# Get the corresponding eigenvector
v2 = list(v[:,w2i])

# Sort the vertces according to v2
for i in range(len(v2)):
	v2[i]=[v2[i],i]
v2.sort()
sorted_vert = []
for ve in v2: sorted_vert.append(ve[1])

Xv=set(Xv)
Yv=set(Yv)

# Reconstruct the partition
clusters = [set(),set()]
for i in range(X+Y):
	if v[:,w2i][i]>0:
		clusters[0].add(i)
	else:
		clusters[1].add(i)

if len(Xv.intersection(clusters[0])) + len(Yv.intersection(clusters[1])) < len(Xv.intersection(clusters[1])) + len(Yv.intersection(clusters[0])):
	tmp = clusters[0]
	clusters[0] = clusters[1]
	clusters[1] = tmp

# Compare with the planted partition
fraction = (len(Xv.intersection(clusters[0])) + len(Yv.intersection(clusters[1])))/float(X+Y)
print str(fraction*100) + " % Correct (" +str(len(Xv.intersection(clusters[0])) + len(Yv.intersection(clusters[1])))+ " out of " + str (X+Y) +") p = " +str(p)+" e = " + str(e) 

