#protVis: application to showcase and compare various proteins

import OpenGL, sys, getopt 
from prody import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#create initial window parameters
width = 500
height = 500
spin_bool = True
(view_rotx,view_roty,view_rotz,view_zoom)=(20.0, 30.0, 0.0,1.0)
#fetch PDB data
id = raw_input("Please enter a protein ID string: ")
filename = fetchPDB(id)
atoms = parsePDB(filename)
coords = atoms.getCoords()
poly = False
line = False
#max/mins

class Stats(object):
    maxX = coords[0][0]
    maxY = coords[0][1]
    maxZ = coords[0][2]
    minX = maxX-1
    minY = maxY-1
    minZ = maxZ-1
    meanX = 0
    meanY = 0
    meanZ = 0

def Scale():
#find max and min for each range
    for a in coords:
        #print(a[2])
        if(a[0] < Stats.minX):
            Stats.minX = a[0]
        elif(a[0] > Stats.maxX):
            Stats.maxX = a[0]
        if(a[1] < Stats.minY):
            Stats.minY = a[1]
        elif(a[1] > Stats.maxY):
            Stats.maxY = a[1]
        if(a[2] < Stats.minZ):
            Stats.minZ = a[2]
        elif(a[2] > Stats.maxZ):
            Stats.maxZ = a[2]
    #multiply projection matrix
    quoX = Stats.maxX - Stats.minX
    quoY = Stats.maxY - Stats.minY
    quoZ = Stats.maxZ - Stats.minZ
    quoN = max(quoZ,max(quoX,quoY))
    Stats.meanX = (Stats.maxX + Stats.minX)/2
    Stats.meanY = (Stats.maxY + Stats.minY)/2
    Stats.meanZ = (Stats.maxZ + Stats.minZ)/2
    for a in coords:
        a[0] = -1+(a[0]-Stats.minX)*(1-(-1))/(quoN)
        #print(a[0])
        a[1] = -1+(a[1]-Stats.minY)*(1-(-1))/(quoN)
        #print(a[1])
        a[2] = -1+(a[2]-Stats.minZ)*(1-(-1))/(quoN)
        #print(a[2])
    

def drawAtom(atom):
    x = atom[0]
    y = atom[1]
    z = atom[2]
    if(z > .5):
      glColor3d(1,0,z)
    elif(z < 0):
      glColor3d(0,1,-z)
    glBegin(GL_POINTS)
    glVertex3fv(atom)
    glEnd()  

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    #rotate points based on key presses
    glRotatef(view_rotx, 1.0, 0.0, 0.0)
    glRotatef(view_roty, 0.0, 1.0, 0.0)
    glRotatef(view_rotz, 0.0, 0.0, 1.0)
    if(view_zoom > 1.0):
      glPointSize(view_zoom)
    else:
      glPointSize(1.0)
    for atom in coords:
        drawAtom(atom)
    glutSwapBuffers()

def key(k, x, y):
    global view_zoom
    global spin_bool
    if k == 'z':
        view_zoom += 1.0
    elif k == 'Z':
        view_zoom -= 1.0
    elif ord(k) == 27: # Escape
        sys.exit(0)
    elif ord(k) == 32:
        spin_bool = not spin_bool
    else:
        return
    glutPostRedisplay()

def special(k, x, y):
    global view_rotx, view_roty, view_rotz
    
    if k == GLUT_KEY_UP:
        view_rotx += 5.0
    elif k == GLUT_KEY_DOWN:
        view_rotx -= 5.0
    elif k == GLUT_KEY_LEFT:
        view_roty += 5.0
    elif k == GLUT_KEY_RIGHT:
        view_roty -= 5.0
    else:
        return
    glutPostRedisplay()

def idle():
  global view_rotz
  if(spin_bool):
      view_rotz += 0.5
  draw()

def init():
    for arg in sys.argv:
	  print(arg)
    try:
      opts, args = getopt.getopt(sys.argv,"hlp", ["help","line","poly"])
    except getopt.GetoptError:
      print "Error. Try -h"
      sys.exit(2)
    for opt,arg in opts:
      if opt in ("h","--help"):
        print "the following are valid arguments: -h, -l, -p"
        sys.exit()
      elif opt in ("-l","--line"):
        global line
        line = True
      elif opt in ("-p","--poly"):
        global poly
        poly = True
    print(line)
    print(poly)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(width,height)
    glutCreateWindow(b"CycloVis")
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluLookAt(0.0,0.0,0.0, 0.5,0.5,1.0, 0.0,1.0,0.0)
    gluPerspective(20.0,width/height,Stats.minZ-10,Stats.maxZ+10)
    Scale()

if __name__ == '__main__':

#initialize
    init()
    glutDisplayFunc(draw)
    glutKeyboardFunc(key)
    glutSpecialFunc(special)
    glutIdleFunc(idle)
    if "-vers" in sys.argv:
      print ("GL_VERSION = ", glGetString(GL_VERSION))

    glutMainLoop()
