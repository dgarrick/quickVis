#CycloVis: application to showcase and compare various proteins in the Cyclophilin family
#TODO: Scale coordinate data so it actually shows up :P
import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from prody import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import sys, time 
from math import sin,cos,sqrt,pi
from OpenGL.constants import GLfloat
vec = GLfloat_3

#create initial window parameters
window = 0
width, height = 300,400
#fetch PDB data
filename = fetchPDB("1cwa")
atoms = parsePDB(filename)
coords = atoms.getCoords()
scaleX = 10
scaleY = 10
scaleZ = 10

def drawAtom(atom):
    glBegin(GL_POINTS)
    x = atom[0]+scaleX
    y = atom[1]+scaleY
    z = atom[2]+scaleZ
    glVertex2f(x,y)
    glEnd()  

	
def scale():
    n = 0
    minX = 0
    minY = 0
    minZ = 0
    maxX = 0
    maxY = 0
    maxZ = 0
    while (n < (coords.size/3)-1):
        if(coords[n][0] < minX):
          minX = coords[n][0]
          print("minX", minX)
        if(coords[n][0] > maxX):
          maxX = coords[n][0]
        if(coords[n][1] < minY):
          minY = coords[n][1]
        if(coords[n][1] > maxY):
          maxY = coords[n][1]
        if(coords[n][2] < minZ):
          minZ = coords[n][2]
        if(coords[n][2] > maxZ):
          maxZ = coords[n][2]
        n+=1
    print("Minimums: ")
    print(minX,minY,minZ)
    print("Maximums: ")
    print(maxX,maxY,maxZ)
    scaleX = -2*minX
    scaleY = -2*minY
    scaleZ = -2*minZ

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh3d(width,height)
    glColor3f(0.0, 0.0, 1.0)
    print("hi")
    for atom in coords:
        drawAtom(atom)
    glutSwapBuffers()

def refresh3d(width,height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()	

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(width,height)
    glutCreateWindow(b"CycloVis")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutReshapeFunc(refresh3d)
    scale()
	
if __name__ == '__main__':

#initialize
    init()
	
    if "-vers" in sys.argv:
        print ("GL_VERSION    = ", glGetString(GL_VERSION))

    glutMainLoop()