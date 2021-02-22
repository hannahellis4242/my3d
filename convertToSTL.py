import json
import numpy as np

def calculateNormal(a,b,c):
    return np.cross(np.subtract(b,a),np.subtract(c,a))

def normalise(x):
    return x/np.linalg.norm(x)

class Facet:
    def __init__(self,vertices):
	self.vertices = vertices
        self.normal = normalise(calculateNormal(vertices[0],vertices[1],vertices[2]));
    def toSTL(self):
	out = ""
        out = out + "facet normal "
        out = out + str(self.normal[0])+" "
        out = out + str(self.normal[1])+" "
        out = out + str(self.normal[2])+"\n"
        out = out + "\touter loop\n"
        for v in self.vertices:
            out = out + "\t\tvertex " + str(v[0])+ " "
            out = out + str(v[1])+ " "
            out = out + str(v[2])+ "\n"
        out = out + "\tendloop\n"
        out = out + "endfacet\n"
        return out

with open('test.json') as json_file:
    data = json.load(json_file)
    print("file has been read")
    solid = data["solid"]
    print("loading")
    vertices = dict()
    count = 0 ;
    total = len(solid["vertex data"])
    for vertex in solid["vertex data"]:
        count=count+1
        print("loading vertex "+str(count) + " of " + str(total))
        id=vertex["id"]
        x=float(vertex["x"])
        y=float(vertex["y"])
        z=float(vertex["z"])
        vertices[id]=[x,y,z]

    print("loading faces")
    facets=[]
    count = 0
    total = len(solid["faces"])
    for face in solid["faces"]:
        count=count+1
        print("loading face " + str(count) +" of " +str(total))
        vs = face["vertices"];
        if face["type"]=="triangle":
            a = vertices[vs[0]]
            b = vertices[vs[1]]
            c = vertices[vs[2]]
            facets.append(Facet([a,b,c]))
        if face["type"]=="quad":
            a = vertices[vs[0]]
            b = vertices[vs[1]]
            c = vertices[vs[2]]
            d = vertices[vs[3]]
            facets.append(Facet([a,b,c]))
            facets.append(Facet([a,c,d]))

    print("creating stl")
    file = open("test.stl","w")
    file.write("solid "+solid["name"]+"\n")
    for facet in facets:
        file.write(facet.toSTL())
    file.write("endsolid "+solid["name"]+"\n")
    file.close()
    print("done")
