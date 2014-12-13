#protVis: application to showcase and compare various proteins

import OpenGL, sys, getopt 
from prody import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#create initial window parameters and camera values
width = 500
height = 500
spin_bool = True
(view_rotx,view_roty,view_rotz,view_zoom)=(20.0, 30.0, 0.0,1.0)
maxX = 0
maxY = 0
maxZ = 0
minX = 0
minY = 0
minZ = 0
meanX = 0
meanY = 0
meanZ = 0
coords = [0][0]

class Args(object):
    poly = False
    line = False
    seq = ""
    id = ""
    isSeq = False

def getAtoms(id):
    try:
      filename = fetchPDB(id)
      atoms = parsePDB(filename)
      if(Args.isSeq):
        sequence(atoms.select("sequence "+Args.seq))
      #coords = atoms.getCoords()
    except TypeError:
      print "Error: invalid ID. Try -h for help."
      sys.exit(2)
    return atoms;

def Scale():
    global maxX, maxY, maxZ, minX, minY, minZ, meanX, meanY, meanZ, atoms, coords;
    #find max and min for each range
    coords = atoms.getCoords()
    for a in coords:
	#print(a[2])
	if(a[0] < minX):
	    minX = a[0]
	elif(a[0] > maxX):
	    maxX = a[0]
	if(a[1] < minY):
	    minY = a[1]
	elif(a[1] > maxY):
	    maxY = a[1]
	if(a[2] < minZ):
	    minZ = a[2]
	elif(a[2] > maxZ):
	    maxZ = a[2]
    #multiply projection matrix
    quoX = maxX - minX
    quoY = maxY - minY
    quoZ = maxZ - minZ
    quoN = max(quoZ,max(quoX,quoY))
    meanX = (maxX + minX)/2
    meanY = (maxY + minY)/2
    meanZ = (maxZ + minZ)/2
    for a in coords:
	a[0] = -1+(a[0]-minX)*(1-(-1))/(quoN)
	#print(a[0])
	a[1] = -1+(a[1]-minY)*(1-(-1))/(quoN)
	#print(a[1])
	a[2] = -1+(a[2]-minZ)*(1-(-1))/(quoN)
	#print(a[2])
    atoms.setCoords(coords)


def drawAtom(atom):
    coords = atom.getCoords()
    x = coords[0]
    y = coords[1]
    z = coords[2]
    #print(x,y,z)
    if(atom.iswater):
      glColor3d(0,0,5)
    elif(atom.isprotein):
      glColor3d(0,5,0)
    elif(atom.isoxygen):
      glColor3d(5,0,0)
    else:
      glColor3d(0,1,1)
    glBegin(GL_POINTS)
    glVertex3fv(coords)
    glEnd()  

def draw():
    global atoms
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
    for atom in atoms:
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
    #gluPerspective(20.0,width/height,minZ-10,maxZ+10)
    

def handleArgs(argv):
    try:
      opts, args = getopt.getopt(argv,"i:hls:", ["id=""help","line","seq="])
    except getopt.GetoptError:
      print "Error. Try -h"
      sys.exit(2)
    for opt,arg in opts:
      if opt in ("-h","--help"):
	print "the following are valid arguments: -i, -s, -h."
	print "-i is required and must be followed by a valid protein ID."
	print "-s is optional but must be followed by an amino acid sequence."
	#print "-l is for a line-based rendering. Useful when combined with an amino acid sequence."
      if opt in ("-i", "--id="):
	Args.id = arg
      if opt in ("-s","--seq="):
	Args.seq = arg
	Args.isSeq = True
      #if opt in ("-l","--line"):
	#Args.line = True



if __name__ == '__main__':

#initialize
    handleArgs(sys.argv[1:])
    atoms = getAtoms(Args.id)
    Scale()
    init()
    
    glutDisplayFunc(draw)
    glutKeyboardFunc(key)
    glutSpecialFunc(special)
    glutIdleFunc(idle)
    if "-vers" in sys.argv:
      print ("GL_VERSION = ", glGetString(GL_VERSION))

    glutMainLoop()
