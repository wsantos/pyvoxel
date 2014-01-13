# coding: utf-8
from mathy import Vector3, Matrix
import ctypes
import pyglet

class Camera(object):
    def __init__(self, position=Vector3(), target=Vector3()):
        self.position = position
        self.target = target


class Mesh(object):

    def __init__(self, name, verticesCount):
        self.vertices = [Vector3()] * verticesCount
        Name = name

class Device(object):

    def __init__(self):
        self.rot = 0.0
        self.BackBuffer = ctypes.c_ubyte * (640*480*4)
        pxbuf = self.BackBuffer()

        self.pxbuf = pxbuf
        self.z_cam = 0.1
        #self.back_buffer = bytearray([0] * bmp.pixel_width * bmp.pixel_height * 4)


    def clear(self, r=0,g=0,b=0,a=0):
        self.pxbuf = self.BackBuffer()

    def present(self):
        pyglet.gl.glDrawPixels(640,480,
                               pyglet.gl.GL_RGBA,
                               pyglet.gl.GL_UNSIGNED_BYTE,
                               self.pxbuf)

    #TODO: Change RGBA to color class
    #TODO: remove 640
    def put_pixel(self, x, y, r, g, b, a):
        index = (x + y * 640) * 4

        if x >= 0 and y >= 0 and x < 640 and y < 480:
            try:

                self.pxbuf[index] = r
                self.pxbuf[index + 1] = g
                self.pxbuf[index + 2] = b
                self.pxbuf[index + 3] = a

            except:
                pass
                #print "index:", index

    def project(coord, transMat):
        pass


