# coding: utf-8
import math
import numpy as np

def cot(theta):
    return 1.0/math.tan(theta)

cot = lambda theta: 1.0 / math.tan(theta)

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
    def transform_coordinate(self, tm):
        vect = Vector3()
        #print "==================="
        #print transform_matrix
        #print self
        va = (self.x * tm.data[0,0]) + (self.y * tm.data[1,0]) +  (self.z * tm.data[2,0]) + tm.data[3,0]
        vb = (self.x * tm.data[0,1]) + (self.y * tm.data[1,1]) +  (self.z * tm.data[2,1]) + tm.data[3,1]
        vc = (self.x * tm.data[0,2]) + (self.y * tm.data[1,2]) +  (self.z * tm.data[2,2]) + tm.data[3,2]
        #print "a=",a,"b=",b,"c=",c

        vd = 1.0 / ((self.x * tm.data[0,3]) + (self.y * tm.data[1,3]) + (self.z * tm.data[2,3])+tm.data[3,3])

        return Vector3(va*vd,vb*vd, self.z  ) # passin z to debug purpose --vc*vd)

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

        data = np.matrix([
            [xaxis.x, yaxis.x, zaxis.x, 0],
            [xaxis.y, yaxis.y, zaxis.y, 0],
            [xaxis.z, yaxis.z, zaxis.z, 0],
            [-(camera_pos * xaxis), -(camera_pos * yaxis), -(camera_pos * zaxis), 1],
        ])
        return Matrix(data.T)

    def __mul__(self, other):

        data = np.matrix(np.zeros(shape=(4,4)))
        other = other.data
        sdata = self.data

        data[0,0] = (sdata[0,0] * other[0,0]) + (sdata[0,1] * other[1,0]) + (sdata[0,2] * other[2,0]) + (sdata[0,3] * other[3,0])
        data[0,1] = (sdata[0,0] * other[0,1]) + (sdata[0,1] * other[1,1]) + (sdata[0,2] * other[2,1]) + (sdata[0,3] * other[3,1])
        data[0,2] = (sdata[0,0] * other[0,2]) + (sdata[0,1] * other[1,2]) + (sdata[0,2] * other[2,2]) + (sdata[0,3] * other[3,2])
        data[0,3] = (sdata[0,0] * other[0,3]) + (sdata[0,1] * other[1,3]) + (sdata[0,2] * other[2,3]) + (sdata[0,3] * other[3,3])
        data[1,0] = (sdata[1,0] * other[0,0]) + (sdata[1,1] * other[1,0]) + (sdata[1,2] * other[2,0]) + (sdata[1,3] * other[3,0])
        data[1,1] = (sdata[1,0] * other[0,1]) + (sdata[1,1] * other[1,1]) + (sdata[1,2] * other[2,1]) + (sdata[1,3] * other[3,1])
        data[1,2] = (sdata[1,0] * other[0,2]) + (sdata[1,1] * other[1,2]) + (sdata[1,2] * other[2,2]) + (sdata[1,3] * other[3,2])
        data[1,3] = (sdata[1,0] * other[0,3]) + (sdata[1,1] * other[1,3]) + (sdata[1,2] * other[2,3]) + (sdata[1,3] * other[3,3])
        data[2,0] = (sdata[2,0] * other[0,0]) + (sdata[2,1] * other[1,0]) + (sdata[2,2] * other[2,0]) + (sdata[2,3] * other[3,0])
        data[2,1] = (sdata[2,0] * other[0,1]) + (sdata[2,1] * other[1,1]) + (sdata[2,2] * other[2,1]) + (sdata[2,3] * other[3,1])
        data[2,2] = (sdata[2,0] * other[0,2]) + (sdata[2,1] * other[1,2]) + (sdata[2,2] * other[2,2]) + (sdata[2,3] * other[3,2])
        data[2,3] = (sdata[2,0] * other[0,3]) + (sdata[2,1] * other[1,3]) + (sdata[2,2] * other[2,3]) + (sdata[2,3] * other[3,3])
        data[3,0] = (sdata[3,0] * other[0,0]) + (sdata[3,1] * other[1,0]) + (sdata[3,2] * other[2,0]) + (sdata[3,3] * other[3,0])
        data[3,1] = (sdata[3,0] * other[0,1]) + (sdata[3,1] * other[1,1]) + (sdata[3,2] * other[2,1]) + (sdata[3,3] * other[3,1])
        data[3,2] = (sdata[3,0] * other[0,2]) + (sdata[3,1] * other[1,2]) + (sdata[3,2] * other[2,2]) + (sdata[3,3] * other[3,2])
        data[3,3] = (sdata[3,0] * other[0,3]) + (sdata[3,1] * other[1,3]) + (sdata[3,2] * other[2,3]) + (sdata[3,3] * other[3,3])

        return Matrix(data)


    @classmethod
    def projection(cls):
        field_of_view = 78
        aspect_ratio = 640 / 480
        near_plane = 0.01
        far_plane = 100.0
        theta_over2 = math.tan(field_of_view * math.pi / 360)

        data = np.matrix(np.identity(4), copy=False)

        data[0,0] = 1 / theta_over2
        data[1,1] = aspect_ratio / theta_over2
        data[2,2] = (near_plane + far_plane) / (near_plane - far_plane)
        data[3,2] = 2 * near_plane * far_plane / (near_plane - far_plane)
        data[2,3] = -1
        data[3,3] = 0

        return Matrix(data)



    @classmethod
    def identity(cls):
        return Matrix(np.matrix(np.identity(4)))


    def __repr__(self):
        # Just for debugging
        return str(self.data)


