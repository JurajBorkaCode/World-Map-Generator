from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
import random

class Polygon_map:
    def __init__(self,x:int,y:int) -> None:
        self.x = x
        self.y = y
        self.poly_map = None
        self.definition = None

    def create_poly_map(self,definition:int) -> None:
        points = self.x*np.random.random((definition,2))
        self.poly_map = Voronoi(points)
        self.definition = definition

    def save_map(self) -> None:
        fig = voronoi_plot_2d(self.poly_map)
        fig.set_size_inches(20,20)
        print(1)
        plt.savefig("poly_map.png")

    def check_vert(self,vertices:int) -> bool:
        for group in vertices:
            if (any(x<0 or x> self.x for x in group)):
                return False
        return True

    def generate_topo(self) -> None:
        fig, ax = plt.subplots(1)
        new_poly = []
        for poly in self.poly_map.regions:
            if poly != []:
                vert = self.poly_map.vertices[poly]
                if self.check_vert(vert):
                    polygon = Polygon(vert, closed=True)
                    new_poly.append(polygon)

        merge = PatchCollection(new_poly)
        ax.add_collection(merge)

        cmap = plt.get_cmap('autumn')
        colours = cmap(np.random.rand(5))

        merge.set_color(colours)
        merge.set_edgecolor("k")
        merge.set_clim([3,50])

        ax.autoscale_view()
        fig.set_size_inches(20,20)
        plt.axis("off")
        fig.savefig("poly_map.png", dpi=fig.dpi, transparent=True)


    def test(self) -> None:
        fig, ax = plt.subplots(1)
        town_center = []
        town_center_arr = self.poly_map.regions[(random.randint(int(self.definition*0.3),int(self.definition*0.7)))]
        print(town_center_arr)

        for j, poly in enumerate(self.poly_map.regions):
            #print(i,self.poly_map.vertices[poly])
            if poly != []:
                #print(poly)
                vert = self.poly_map.vertices[poly]
                for i in poly:
                    #print(i)
                    if i in town_center:
                        print("HH")

                    if self.check_vert(vert):
                        new_poly = Polygon(vert, closed=True)
                        town_center.append(new_poly)
                        town_center_arr.append(vert)

        #print(town_center_arr)
        #print(town_center)



        out = PatchCollection(town_center)
        ax.add_collection(out)

        out.set_color([1, 0, 0])
        out.set_edgecolor("k")
        out.set_clim([3,50])

        ax.autoscale_view()
        fig.set_size_inches(20,20)
        plt.axis("off")
        fig.savefig("poly_map.png", dpi=fig.dpi, transparent=True)


a = Polygon_map(100,100)
a.create_poly_map(2000)
a.test()
#a.generate_topo()
#a.save_map()