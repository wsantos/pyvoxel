from __future__ import division
import math
import itertools
import sys
from random import randint
import timeit
import pyglet
from pyglet import image
import ctypes
import numpy as np

FORMAT = 'RGBA'

def cot(theta):
    return 1.0/math.tan(theta)

class Vector3(object):
    __slots__ = ("x", "y", "z")
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    #def __len__(self):
        #return math.sqrt(self.x*self.x + self.y*self.y)

    @property
    def lenght(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def __repr__(self):
        return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)

    #def __rdiv__(self, other):
        #return Vector3(self.x / other, self.y / other, self.z / other)

    def __div__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)

    def __truediv__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)


    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    @classmethod
    def unit_x(cls):
        return cls(1.0, .0, .0)

    @classmethod
    def unit_y(cls):
        return cls(.0, 1.0, .0)

    @classmethod
    def unit_z(cls):
        return cls(.0, .0, 1.0)

    def normalized(self):
        return self / self.lenght

    #List like
    def __len__(self):
        return 3

    def __iter__(self):
        for i in xrange(3):
            yield self[i]
        raise StopIteration

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            return self.z

class Matrix(object):

    def __init__(self, data=None):

        if not data is None:
            self.data = data
        else:
            self.data = np.zeros(shape=(4,4))

    @classmethod
    def look_at(cls, camera_pos, camera_target, unit):

        zaxis = (camera_target - camera_pos).normalized()
        xaxis = Vector3(*np.cross(unit, zaxis)).normalized()
        yaxis = Vector3(*np.cross(zaxis, xaxis))

        data = np.array([
            [xaxis.x, yaxis.x, zaxis.x, 0],
            [xaxis.y, yaxis.y, zaxis.y, 0],
            [xaxis.z, yaxis.z, zaxis.z, 0],
            [-(camera_pos * xaxis), -(camera_pos * yaxis), -(camera_pos * zaxis), 1],
        ])
        return Matrix(data)

    @classmethod
    def projection(cls):
        field_of_view = 78
        near_plane = 0.01
        far_plane = 1.0
        aspect_ratio = 640 / 480

        y_scale = cot(field_of_view / 2)
        x_scale = y_scale / aspect_ratio

        frustum_length = far_plane - near_plane

        projection_matrix = np.zeros(shape=(4,4))

        projection_matrix[0][0] = x_scale
        projection_matrix[1][1] = y_scale
        projection_matrix[2][2] = -((far_plane + near_plane) / frustum_length)
        projection_matrix[2][3] = -1
        projection_matrix[3][2] = -((2 * near_plane * far_plane) / frustum_length)

        return Matrix(projection_matrix)


    @classmethod
    def identity(cls):
        return Matrix(np.identity(4))


    def __repr__(self):
        # Just for debugging
        return str(self.data)

### Common Class helpers - Need change

class WriteableBitmap(object):

    def __init__(self, width=0, heigth=0):
        self.width = width
        self.heigth = heigth

    @property
    def pixel_width(self):
        return self.width

    @property
    def pixel_height(self):
        return self.heigth


###



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
        BackBuffer = ctypes.c_ubyte * (640*480*4)
        pxbuf = BackBuffer()

        self.pxbuf = pxbuf
        #self.back_buffer = bytearray([0] * bmp.pixel_width * bmp.pixel_height * 4)


    def clear(self, r=0,g=0,b=0,a=0):
        #User pyglet clear
        pass

    def present(self):
        pyglet.gl.glDrawPixels(640,480,
                               pyglet.gl.GL_RGBA,
                               pyglet.gl.GL_UNSIGNED_BYTE,
                               self.pxbuf)

    #TODO: Change RGBA to color class
    #TODO: remove 640
    def put_pixel(self, x, y, r, g, b, a):
        index = (x + y * 640) * 4

        try:

            self.pxbuf[index] = r
            self.pxbuf[index + 1] = g
            self.pxbuf[index + 2] = b
            self.pxbuf[index + 3] = a

        except:
            print "index:", index

    def project(coord, transMat):
        pass

def main():

    cp = Vector3(0,0,10.0)
    ct = Vector3(0,0,0)


    view_matrix = Matrix.look_at(cp, ct, Vector3.unit_y())
    projection_matrix = Matrix.projection()

    window = pyglet.window.Window()

    pxbuf = image.ImageData(640, 480, "RGBA", None)

    data = [chr(0),chr(0),chr(0),chr(0)] * int(pxbuf.height * pxbuf.pitch / 4)
    pxbuf.set_data("RGBA", pxbuf.pitch, "".join(data))

    device = Device()

    mesh = Mesh("Cube", 8)
    mesh.vertices[0] = Vector3(-1, 1, 1)
    mesh.vertices[1] = Vector3(1, 1, 1)
    mesh.vertices[2] = Vector3(-1, -1, 1)
    mesh.vertices[3] = Vector3(-1, -1, -1)
    mesh.vertices[4] = Vector3(-1, 1, -1)
    mesh.vertices[5] = Vector3(1, 1, -1)
    mesh.vertices[6] = Vector3(1, -1, 1)
    mesh.vertices[7] = Vector3(1, -1, -1)


    #render loop
    @window.event
    def on_draw():
        start = timeit.default_timer()
        window.clear()



        x = randint(0,640)
        y = randint(0,480)

        device.put_pixel(x,y,0,255,0,0)
        device.present()

        #pxbuf.blit(0, 0)

        stop = timeit.default_timer()
        time = stop - start
        if time > 0.016:
            print "Drop"


    def update(dt):
        pass

    pyglet.clock.schedule_interval(update, 0.0001)


    pyglet.app.run()

    #start = timeit.default_timer()
    #stop = timeit.default_timer()
    #print stop - start

if __name__ == "__main__":
    sys.exit(main())
