import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes
from bubblesort import bubbleSort


class App:


    def __init__(self, list):

        #initialize Python
        pg.init()
        self.window = pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        #initialize OpenGL
        glClearColor(0.1, 0.1, 0.1, 1)

        #specify Font for characters
        self.font = pg.font.SysFont('Arial', 12)

        #initialize shaders
        self.shader = self.createShader('my_project/sorting_openGL_shaders/vertex.txt', 'my_project/sorting_openGL_shaders/fragment.txt')
        glUseProgram(self.shader)
        self.axes = Axes()

        #bubbleSort list
        self.sorted_list_length = len(list)
        self.iterated_lists = bubbleSort(list)
        self.iteration_count = int(len(self.iterated_lists)/self.sorted_list_length)

        #Camera initial starting position + rotation
        self.cameraPos = [0.0, 0.0, -0.5]
        self.cameraRot = [0.0, 0.0, 0.0] 

        #make list containing lists (each entry is a list of one iteration of Bubblesort)
        self.all_bars = [None] * self.iteration_count
        position = 0
        bar_list_no = 0
        
        for value in self.iterated_lists:
            if (position == 0):
                bars = [None] * self.sorted_list_length

            bars[position] = Bar(position, value)
            print()
            #print("POSITION: " + str(bars[position].realPos))
            #print("value: " + str(bars[position].realVal))
            position = position + 1
            if (position >= self.sorted_list_length):
                self.all_bars[bar_list_no] = bars
                #print("liste nr " + str(bar_list_no) + " fertig")
                bar_list_no = bar_list_no + 1
                position = 0

        #print
        nr = 0
        for i in self.all_bars:
            print()
            print("Liste nr. " + str(nr) + " anfang")
            nr = nr + 1
            for j in i:
                print("POSITION: " + str(j.realPos))
                print("value: " + str(j.realVal))

            
            
        
        # for taking screenshots
        for i in range(len(self.all_bars)):
            #print(str(i) + " screenshot started")
            self.snapshot(self.all_bars[i], i)
            #print(str(self.all_bars[i]))
            #print(str(i) + " screenshot finished")

        #pg.display.flip()

        # for making the Pygame window view
        self.mainLoop()


    
    
    def mainLoop(self):

        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False


            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            #draw coordinate system
            glUseProgram(self.shader)

            glBindVertexArray(self.axes.vao)
            glDrawArrays(GL_LINES, 0, self.axes.vertex_count)
            glBindVertexArray(0)

            for i in range(len(self.all_bars)):
                bars = [None] * self.sorted_list_length
                for j in range(len(self.all_bars[i])):
                    #draw bars of each iteration:
                    bars = self.all_bars[i]
                    glBindVertexArray(bars[j].vao)
                    glDrawArrays(GL_QUADS, 0, bars[j].vertex_count)
                    glBindVertexArray(0)
                    #print(str(bars[j].value) + " DRAWN")

            #Camera
            keys = pg.key.get_pressed()
            #Camera movement
            
            
            pg.display.flip()
            #timing
            self.clock.tick(60)

        self.quit()

    
    def capture_screen(self, title):

        """ pg.display.set_allow_screensaver(True)
        print(pg.display.get_allow_screensaver()) """

        """ width, height = pg.display.get_surface().get_size()
        screenshot = pg.surfarray.pixels3d(pg.display.get_surface())
        print(screenshot)
        pg.image.frombuffer(screenshot, (width, height), 'RGB').save(f"sorting/images/screenshot_{title}.png") """

        """ display = pg.display.get_surface()
        print(display)
        screencopy = display.copy() 
        print("screencopy: ")
        print(screencopy) """

        """ display = pg.PixelArray.make_surface(640, 480)
        print(display) """

        """ sf = pg.Surface.get_view('3')
        print("surface: " + str(sf)) """
        #pg.image.save(sf, f"sorting/images/screenshot_{title}.png")

        """ canvas = pg.Surface(window.get_size())
        canvas.blit(window, (0,0))
        pg.image.save(canvas, f"sorting/images/screenshot_{title}.png") """

        size = self.window.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        #pg.display.flip()

        screen_surface = pg.image.fromstring(buffer, size, "RGBA", True)
        pg.image.save(screen_surface, f"sorting/images/screenshot_{title}.png")

    
    def snapshot(self, bars, number):

        self.axes = Axes()

        # refresh screen
        glClear(GL_COLOR_BUFFER_BIT)
        #draw coordinate system
        glUseProgram(self.shader)
        glBindVertexArray(self.axes.vao)
        glDrawArrays(GL_LINE_STRIP, 0, self.axes.vertex_count)
        glBindVertexArray(0)

        """ for bars in self.all_bars:
            if((i % number_count) == 0):
                    # make screenshot before clearing canvas:
                    self.capture_screen(image_count, window)
                    # refresh screen
                    glClear(GL_COLOR_BUFFER_BIT)
                    #draw coordinate system
                    glUseProgram(self.shader)

                    glBindVertexArray(self.axes.vao)
                    glDrawArrays(GL_LINE_STRIP, 0, self.axes.vertex_count)
                    glBindVertexArray(0)
                    

                    image_count += 1 """
            
        for i in bars:
            """ print("POSITION: " + str(i.realPos))
            print("value: " + str(i.realVal)) """
            #draw bars of each iteration:
            glBindVertexArray(i.vao)
            glDrawArrays(GL_QUADS, 0, i.vertex_count)
            glBindVertexArray(0)

        self.capture_screen(number)
        


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
        self.axes.destroy()
        for i in range(len(self.all_bars)):
            for j in range(len(self.all_bars[i])):
                self.all_bars[i][j].destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Axes:


    def __init__(self):

        #x, y, z, r, g, b
        self.vertices = (
            -0.8,  0.8, 0.0, 1.0, 0.0, 0.0,     # y- Achse Start-vertice
            -0.8, -0.8, 0.0, 0.0, 1.0, 0.0,     # y-Achse End-vertice
            -0.8, -0.8, 0.0, 0.0, 1.0, 0.0,     # x-Achse Start-vertice
             0.8, -0.8, 0.0, 0.0, 0.0, 1.0,     # x-Achse End-vertice
            -0.8, -0.8, 0.0, 0.0, 1.0, 0.0,     # z-Achse Start-vertice
            -0.8, -0.8, 0.1, 0.0, 1.0, 0.0,     # z-Achse End-vertice
        )

        #format vertices data into data type graphics card can read with numpy:
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 6

        #Create one Vertex Array Object, adds attribute pointers to vbo to interpret data correctly
        self.vao = glGenVertexArrays(1)
        #IMPORTANT: always bind VAO before VBO. Doing that, the VAO knows which VBO to work with
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
        # offset for where data begins for the first point, presented as special C-type pointer: first (position) starts at 0 and second (color) starts at 3*4 bytes;
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


    def destroy(self):

        #this function expects us to give it a list so we have to wrap it in list type
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


class Bar:


    def __init__(self, position, value):
        
        #fordebugging
        self.realVal = value
        self.realPos = position
        
        self.position = -0.8 + (position * 0.1)
        self.value = -0.8 + (value * 0.015)

        self.vertices = (
            self.position,        -0.8,       0.0, 0.0, 0.0, 1.0,
            self.position + 0.05, -0.8,       0.0, 0.0, 0.0, 1.0,
            self.position + 0.05, self.value, 0.0, 1.0, 0.0, 0.0,
            self.position,        self.value, 0.0, 1.0, 0.0, 0.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 4

        #Create one Vertex Array Object, adds attribute pointers to vbo to interpret data correctly
        self.vao = glGenVertexArrays(1)
        #IMPORTANT: always bind VAO before VBO. Doing that, the VAO knows which VBO to work with
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
        # offset for where data begins for the first point, presented as special C-type pointer: first (position) starts at 0 and second (color) starts at 3*4 bytes;
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


    def destroy(self):

        #this function expects us to give it a list so we have to wrap it in list type
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

    

#data = [-2, 45, 5, 11, -9]
data = [1, 4, 0, 3, 2, 5]

if __name__ == "__main__":
    myApp = App(data)
