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

def findVertexById( id , localVertices , globalVertices ):
    if id in localVertices:
        return localVertices[id]
    if id in globalVertices:
        return globalVertices[id]
    return None

def faceToFacet(face,globalVertices,localVertices):
    vs = face["vertices"];
    if face["type"]=="triangle":
        a = findVertexById(vs[0],globalVertices,localVertices)
        b = findVertexById(vs[1],globalVertices,localVertices)
        c = findVertexById(vs[2],globalVertices,localVertices)
        return [Facet([a,b,c])]
    if face["type"]=="quad":
        a = findVertexById(vs[0],globalVertices,localVertices)
        b = findVertexById(vs[1],globalVertices,localVertices)
        c = findVertexById(vs[2],globalVertices,localVertices)
        d = findVertexById(vs[3],globalVertices,localVertices)
        return [Facet([a,b,c]),Facet([a,c,d])]
    return []

def loadVertices( vertices ):
    out = dict()
    count = 0 ;
    total = len(vertices)
    for vertex in vertices:
        count=count+1
        print("loading vertex "+str(count) + " of " + str(total))
        id=vertex["id"]
        x=float(vertex["x"])
        y=float(vertex["y"])
        z=float(vertex["z"])
        out[id]=[x,y,z]
    return out;

def loadFaces( faces , globalVertices , localVertices ):
    count = 0
    total = len(solid["faces"])
    facets=[]
    for face in faces:
        count=count+1
        print("loading face " + str(count) +" of " +str(total))
        facets.extend( faceToFacet( face , globalVertices , localVertices ) )
    return facets

with open('test.json') as json_file:
    data = json.load(json_file)
    print("file has been read")
    solid = data["solid"]
    print("loading")
    globalVertices = loadVertices( solid["global vertices"] )

    facets=[]
    if( "components" in solid ):
        print("has components")
        print("loding components")
        count = 0
        total = len(solid["components"])
        for component in solid["components"]:
            count=count+1
            print("loading component " + component["name"] + "\n\t" + str(count) + " of "+ str(total))
            localVertices=loadVertices( component["vertices"] )
            facets.extend(loadFaces( component["faces"], globalVertices,localVertices ))

    print("loading faces")
    facets.extend(loadFaces(solid["faces"],globalVertices,[]))

    print("creating stl")
    file = open("test.stl","w")
    file.write("solid "+solid["name"]+"\n")
    for facet in facets:
        file.write(facet.toSTL())
    file.write("endsolid "+solid["name"]+"\n")
    file.close()
    print("done")
