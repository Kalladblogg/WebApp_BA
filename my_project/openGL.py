import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader


class App:


    def __init__(self):

        #initialize Python
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        #initialize OpenGL
        glClearColor(0.1, 0.1, 0.1, 1)

        #initialize shaders
        self.shader = self.createShader('my_project/openGL_shaders/vertex.txt', 'my_project/openGL_shaders/fragment.txt')
        glUseProgram(self.shader)
        self.triangle = Triangle()

        self.mainLoop()


    def mainLoop(self):

        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            #draw triangle
            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()


    #take the shaders as string, compile them to a shader module, combine the two modules to a shader Program we can send to the GPU:
    def createShader(self, vertexFilePath, fragmentFilePath):

        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader


    def quit(self):
        
        #clear memory before quitting
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Triangle:

    def __init__(self):

        #x, y, z, r, g, b
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
             0.0,  0.5, 0.0, 0.0, 0.0, 1.0
        )

        #format vertices data into data type graphics card can read with numpy:
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        #Vertex Array Object, adds attribute pointers to vbo to interpret data correctly
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        #Vertex Buffer Object, create one Buffer and gives us the index:
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        #ship vertices to graphics card:
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        #describe Attributes in VBO by enabling first and then describing its layout:
        #Attribute 0 is position and 1 is color
        glEnableVertexAttribArray(0) 
        # how many points in each attribute: 3 colors, 3 positions; 
        # kind of data: float; 
        # potential formatting of data: false; 
        # stride: 6 numbers with each 4 bytes; 
        # offset for where data begins for the first point, presented as special C-type pointer: first (position) starts at 0 and second (color) starts at 3*4;
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


    def destroy(self):

        #this function expects us to give it a list so we have to wrap it in list type
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

    


if __name__ == "__main__":
    myApp = App()

