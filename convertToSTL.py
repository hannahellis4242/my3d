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
    total = len(faces)
    facets=[]
    for face in faces:
        count=count+1
        print("loading face " + str(count) +" of " +str(total))
        facets.extend( faceToFacet( face , globalVertices , localVertices ) )
    return facets

def loadGlobalVertices(solid):
    if "global vertices" in solid:
        return loadVertices( solid["global vertices"] )
    return []

def loadComponents(solid,globalVertices):
    if( "components" in solid ):
        facets=[]
        print("has components")
        print("loding components")
        count = 0
        total = len(solid["components"])
        for component in solid["components"]:
            count=count+1
            print("loading component " + component["name"] + "\n\t" + str(count) + " of "+ str(total))
            localVertices=[]
            if "vertices" in component :
                localVertices = loadVertices( component["vertices"] )
            facets.extend(loadFaces( component["faces"], globalVertices,localVertices ))
        return facets
    return []

def loadGlobalFaces(solid,globalVertices):
    if "faces" in solid:
        return loadFaces( solid["faces"],globalVertices,[] )
    return []

def loadSolid(solid):
    globalVertices = loadGlobalVertices( solid )

    facets=[]
    facets.extend(loadComponents( solid , globalVertices ))
    facets.extend(loadGlobalFaces(solid,globalVertices))

    return facets

def saveFacetsAsSTL( facets , solid , filename):
    file = open(filename,"w")
    file.write("solid "+solid["name"]+"\n")
    for facet in facets:
        file.write(facet.toSTL())
    file.write("endsolid "+solid["name"]+"\n")
    file.close()

with open('test.json') as json_file:
    try:
        data = json.load(json_file)
        print("file has been read")
        print("loading")
        facets=loadSolid(data["solid"]);
        print("creating stl")
        saveFacetsAsSTL( facets, data["solid"], "test.stl" )
        print("done")
    except ValueError as e:
        print(e)
