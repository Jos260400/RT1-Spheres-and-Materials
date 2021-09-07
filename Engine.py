#Universidad del Valle de Guatemala
#Graficas por Computadoras
#Fernando Jose Garavito Ovando 18071
#RT1
#Import
from Raytracing import Raytracer, BLACK, Material, Sphere, V3
from Raytracing import color

#Materiales
Ojos = Material(diffuse=BLACK)
Boca = Material(diffuse=BLACK)
Botones = Material(diffuse=BLACK)
Cuerpo = Material(diffuse=color(255, 255, 255))
Nariz = Material(diffuse=color(255, 108, 0))

#Render
render = Raytracer(500, 500)
render.models = [

#Muñeco de nieve   
    #Cara
    Sphere(V3(0.25, -2, -6), 0.025, Ojos),
    
    Sphere(V3(-0.25, -2, -6), 0.025, Ojos),
    
    Sphere(V3(0, -1.75, -6), 0.15, Nariz),

    Sphere(V3(0.3, -1.55, -6), 0.05, Boca),

    Sphere(V3(-0.3, -1.55, -6), 0.05, Boca),
    
    Sphere(V3(-0.15, -1.5, -6), 0.05, Boca),
    
    Sphere(V3(0.15, -1.5, -6), 0.05, Boca),
        
    #Botones
    Sphere(V3(0, -0.75, -5), 0.1, Botones),
    
    Sphere(V3(0, 0, -5), 0.1, Botones),
    
    Sphere(V3(0, 1.25, -5), 0.1, Botones),
    
    #Cuerpo
    Sphere(V3(0, -3, -10), 1, Cuerpo),
    
    Sphere(V3(0, -1, -10), 1.5, Cuerpo),

    Sphere(V3(0, 2, -10), 2, Cuerpo),
    
]

render.finish()
