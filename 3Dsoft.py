#coding:utf-8
from __future__ import division
import itertools
import sys
import timeit
import pyglet

#Engine
from mathy import Vector3, Matrix
from engine import Device, Mesh


FORMAT = 'RGBA'


def main():
    window = pyglet.window.Window()

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

    mesh2 = Mesh("Quad", 4)
    mesh2.vertices[0] = Vector3(-1, 1, 1)
    mesh2.vertices[1] = Vector3(1, 1, 1)
    mesh2.vertices[2] = Vector3(-1, -1, 1)
    mesh2.vertices[3] = Vector3(1, -1, 1)


    #render loop
    @window.event
    def on_draw():


        cp = Vector3(device.z_cam,0,10.0)
        ct = Vector3(0,0,0)

        #device.z_cam += 0.01
        mesh.rotation.x += 0.01
        mesh.rotation.y += 0.01
        mesh.rotation.z += 0.01
        view_matrix = Matrix.look_at(cp, ct, Vector3.unit_y())
        projection_matrix = Matrix.projection()
        #world_matrix = Matrix.identity()#chamar funcao yaw aqui que recebe o vetor rotation
        world_matrix = Matrix.pyr(mesh.rotation)
        #tm = world_matrix * view_matrix * projection_matrix
        tm = projection_matrix * view_matrix * world_matrix


        start = timeit.default_timer()
        window.clear()
        device.clear()
        #device.rot += 10.1
        #world_matrix.data[2][2] = device.rot
        #print "rot",device.rot
        print "Begin mesh draw -----------------------------------------------"
        for index, vertice in enumerate(mesh.vertices):
            vertice_tmp = vertice.transform_coordinate(tm)
            print vertice_tmp
            x = vertice_tmp.x * 640 + 640/2.0
            y = -vertice_tmp.y * 480 + 480 /2.0
            print "Vertex %s: %s,%s,%s" % (index, x, y, vertice_tmp.z)

            color = None
            if vertice_tmp.z > 0:
                color = (255,0,0,0)
            else:
                color = (0,255,0,0)

            device.put_pixel(int(x),int(y), *color)
        print "End mesh draw -----------------------------------------------"

        #device.put_pixel(5,5,5,255,0,0)
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
