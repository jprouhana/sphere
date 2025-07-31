import math
import pygame
from pygame.locals import *

# --- Vector math ---
class Vec3:
    def __init__(self,x,y,z): self.x,self.y,self.z = x,y,z
    def __add__(self,o):   return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self,o):   return Vec3(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self,t):   return Vec3(self.x*t,   self.y*t,   self.z*t)
    __rmul__ = __mul__
    def __truediv__(self,t): return Vec3(self.x/t, self.y/t, self.z/t)
    def dot(self,o): return self.x*o.x + self.y*o.y + self.z*o.z
    def length(self): return math.sqrt(self.dot(self))
    def normalize(self): return self / self.length()

# --- Ray-sphere intersection & shading ---
def ray_sphere(orig, dir, center, radius):
    oc = orig - center
    a = dir.dot(dir); b = 2*oc.dot(dir)
    c = oc.dot(oc) - radius*radius
    disc = b*b - 4*a*c
    if disc < 0: return -1
    return (-b - math.sqrt(disc)) / (2*a)

def trace_ray(orig, dir, center):
    t = ray_sphere(orig, dir, center, 0.5)
    if t > 0:
        hit = orig + dir*t
        normal = (hit - center).normalize()
        light = Vec3(1,1,-0.5).normalize()
        intensity = max(0, normal.dot(light))
        col = Vec3(1,0,0)*intensity
        return (int(col.x*255), int(col.y*255), int(col.z*255))
    # background
    unit = dir.normalize()
    t_bg = 0.5*(unit.y + 1)
    r = int(((1-t_bg)*1 + t_bg*0.5)*255)
    g = int(((1-t_bg)*1 + t_bg*0.7)*255)
    b = int(((1-t_bg)*1 + t_bg*1  )*255)
    return (r,g,b)

# --- Render low-res into a pygame.Surface ---
def render_to_surface(center, RES):
    surf = pygame.Surface(RES)
    w, h = RES
    orig = Vec3(0,0,0)
    for j in range(h):
        for i in range(w):
            u = (i+0.5)/w*2 - 1
            v = (j+0.5)/h*2 - 1
            dir = Vec3(u, -v, -1).normalize()
            surf.set_at((i,j), trace_ray(orig, dir, center))
    return surf

# --- Main loop ---
def main():
    pygame.init()
    WIN = (600, 600)
    RES = (200, 200)
    screen = pygame.display.set_mode(WIN)
    pygame.display.set_caption("Drag the Sphere")
    
    sphere_center = Vec3(0,0,-1)
    dragging = False
    clock = pygame.time.Clock()

    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT: 
                pygame.quit()
                return
            if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                dragging = True
            if ev.type == MOUSEBUTTONUP and ev.button == 1:
                dragging = False
            if ev.type == MOUSEMOTION and dragging:
                mx, my = ev.pos
                nx = (mx / WIN[0])*2 - 1
                sphere_center = Vec3(nx, 0, -1)
        
        low = render_to_surface(sphere_center, RES)
        screen.blit(pygame.transform.scale(low, WIN), (0,0))
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()

