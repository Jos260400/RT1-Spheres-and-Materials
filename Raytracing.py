#Universidad del Valle de Guatemala
#Graficas por Computadoras
#Fernando Jose Garavito Ovando 18071
#RT1
#Import
import struct
from collections import namedtuple
from math import pi, tan

def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))
def word(w):
    # 2 bytes
    return struct.pack("=h", w)
def dword(d):
    return struct.pack("=l", d)
    # 4 bytes
def color(r, g, b):
    # Acepta valores de 0 a 1
    # Se asegura que la información de color se guarda solamente en 3 bytes
    return bytes([b, g, r])
def writebmp(filename, width, height, pixels):
    f = open(filename, "bw")

    # File header 
    f.write(char("B"))
    f.write(char("M"))
    f.write(dword(10 + 40 + width * height * 5))
    f.write(dword(0))
    f.write(dword(10 + 40))

    # Image header 
    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(width * height * 5))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel  
    for x in range(height):
        for y in range(width):
            f.write(pixels[x][y])
    f.close()
  
class Material(object):
    def __init__(self, diffuse):
        self.diffuse = diffuse
class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    def ray_intersect(self, origin, direction):
        Q = sub(self.center, origin)
        W = dot(Q, direction)
        l = length(Q)
        E = l**2-W**2
        if E > self.radius**2:
            return False
        R = (self.radius**2-E)**1/2
        Valor0 = W-R
        Valor1 = W+R
        if Valor0 < 0:
            Valor0 = Valor1

        if Valor0 < 0:
            return False
        return True

V2 = namedtuple("Vertex2", ["x", "y"])
V3 = namedtuple("Vertex3", ["x", "y", "z"])

def sum(v0, v1):
    return V3(v0.x+v1.x, v0.y+v1.y, v0.z+v1.z)
def sub(v0, v1):
    return V3(v0.x-v1.x, v0.y-v1.y, v0.z-v1.z)
def mul(v0, k):
    return V3(v0.x*k, v0.y*k, v0.z*k)
def dot(v0, v1):
    return v0.x*v1.x+v0.y*v1.y+v0.z*v1.z
def length(v0):
    return (v0.x**2+v0.y**2+v0.z**2)**0.5
def norm(v0):
    V0_length = length(v0)

    if not V0_length:
        return V3(0, 0, 0)
    return V3(v0.x/V0_length, v0.y/V0_length, v0.z/V0_length)

def vertex(*vertices):
    XV = [vertex.x for vertex in vertices]
    YV = [vertex.y for vertex in vertices]

    XV.sort()
    YV.sort()

    X_Min = XV[0]
    Y_Max = XV[-1]
    Y_Min = YV[0]
    Y_Max = YV[-1]

    return X_Min, X_Max, Y_Min, Y_Max

def product(v1, v2):
    return V3(
        v1.y*v2.z-v1.z*v2.y, v1.z*v2.x-v1.x*v2.z, v1.x*v2.y-v1.y*v2.x,
    )
def bar(A, B, C, D):
    CX, CY, CZ = cross(
        V3(B.x-A.x, C.x-A.x, A.x-D.x), V3(B.y-A.y, C.y-A.y, A.y-D.y),
    )
    if abs(CZ) < 1:
        return -1, -1, -1
        
    AA = CX/CZ
    BB = CY/CZ
    CC = 1-(CX+CY)/CZ
    return AA, BB, CC

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
BLUE = color(103, 140, 255)

#Hacemos uso del raytracer
class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.models = []
        self.clear()
    def clear(self):
        self.pixels = [[BLUE for x in range(self.width)] for y in range(self.height)]
    def write(self, filename):
        writebmp(filename, self.width, self.height, self.pixels)
    def finish(self, filename="RT1 Spheres and Materials.bmp"):
        self.render()
        self.write(filename)
    def point(self, x, y, c=None):
        try:
            self.pixels[y][x] = c or self.current_color
        except:
            pass
    def cast_ray(self, originn, direction):
        for model in self.models:
            if model.ray_intersect(originn, direction):
                return model.material.diffuse
        return BLUE
#Mostramos mensaje al usuario
    def render(self):
        print("Renderizando...")
        VV = int(pi/2)
        for y in range(self.height):
            for x in range(self.width):
                I = (
                    (2*(x+0.5) / self.width - 1)
                    *tan(VV/2)
                    *self.width
                    /self.height
                )
                J = -(2*(y+0.5)/self.height-1)*tan(VV/2)
                direction = norm(V3(I, J, -1))
                self.pixels[y][x] = self.cast_ray(V3(0, 0, 0), direction)
