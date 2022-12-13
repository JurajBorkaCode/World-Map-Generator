from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
import random
import networkx
import itertools
import copy
import collections
from PIL import Image

class poly_map:
    def __init__(self,size:int,seed:str=None) -> None:
        random.seed(seed)
        np.random.seed(random.randint(1,1000000))
        self.size = size
        points = size*np.random.random((size**2,2))
        self.poly_map = Voronoi(points)
        self.smooth(5)
        self.districts = {"inner":[],"outer":[],"slums":[]}
        self.walls = 0

    def check(self,vertices:list[list[int]]) -> bool:
        for couple in vertices:
            if (any(x < 0 or x > self.size for x in couple)):
                return False
        return True

    def lloyd_relax(self, times:int) -> Voronoi:
            for i in range(times):
                centroids = []
                for region in self.poly_map.regions:
                    if (region != []):
                        vertices = self.poly_map.vertices[region]
                        if (self.check(vertices)):
                            centroid_x = np.sum(vertices[:, 0])/vertices.shape[0]
                            centroid_y = np.sum(vertices[:, 1])/vertices.shape[0]
                            centroid = [centroid_x, centroid_y]
                            centroids.append(centroid)
            return Voronoi(centroids)

    def smooth(self,amount:int) -> None:
        self.poly_map = self.lloyd_relax(amount)


    def generate_network(self,min_height:int) -> None:
        cell_network = networkx.Graph()

        edges = {}

        for i, region in enumerate(self.poly_map.regions):
            for edge in list(itertools.combinations(region,2)):
                if edge in edges:
                    edges[edge].append(i)
                    edges[edge[::-1]].append(i)
                else:
                    edges[edge] = [i]
                    edges[edge[::-1]] = [i]

        for i in edges:
            for j in edges[i]:
                cell_network.add_node(j,height = min_height, district = "", ter_type = "nat")
            if len(edges[i]) > 1:
                cell_network.add_edge(edges[i][0],edges[i][1])

        ##  remove nodes
        new_net = copy.deepcopy(cell_network)

        for node in cell_network.nodes:
            if not self.check(self.poly_map.vertices[self.poly_map.regions[node]]):
                new_net.remove_node(node)

        self.cell_network = new_net

    def elevation_decrease(self,cell:int,complete_cells:list[int],elevation:int,min_height:int) -> None:
        new_cells = copy.deepcopy(complete_cells)
        for n in self.cell_network.neighbors(cell):
            if (n not in new_cells) or (self.cell_network.nodes[n]["height"] < elevation):
                if self.cell_network.nodes[n]["height"] < elevation:
                    self.cell_network.nodes[n]["height"] = elevation
                    new_cells.append(n)
                    if elevation > min_height:
                        self.elevation_decrease(n,new_cells,elevation-1,min_height)

    def generate_terain(self,max_height:int,min_height:int,min_peak_height:int,number_of_peaks:int) -> None:
        self.generate_network(min_height)
        self.peaks_locs = []

        for i in range(number_of_peaks):
            peak = random.randint(int(self.cell_network.number_of_nodes()*0.3),int(self.cell_network.number_of_nodes()*0.7))
            if self.check(self.poly_map.vertices[self.poly_map.regions[peak]]):
                self.cell_network.nodes[peak]["height"] = random.randint(min_peak_height,max_height)
                self.peaks_locs.append(peak)
                pass

        for peak in self.peaks_locs: 
            self.elevation_decrease(peak,self.peaks_locs,self.cell_network.nodes[peak]["height"],min_height)
        
        self.sort_to_elevation()

    def sort_to_elevation(self) -> None:
        groups = {}

        for i in self.cell_network.nodes:
            height = self.cell_network.nodes[i]["height"]
            if(self.check(self.poly_map.vertices[self.poly_map.regions[i]])):
                if height in groups:
                    groups[height].append(Polygon(self.poly_map.vertices[self.poly_map.regions[i]]))
                else:
                    groups[height] = [Polygon(self.poly_map.vertices[self.poly_map.regions[i]])]

        self.groups = collections.OrderedDict(sorted(groups.items()))

    def map_output_elevation(self) -> None:
        fig, ax = plt.subplots(1)
        deep = []
        water = []
        hills = []
        plains = []
        beach = []
        mountains = []

        for i in self.groups:
            if i > 40:
                mountains.append(PatchCollection(self.groups[i]))
            elif i > 25:
                hills.append(PatchCollection(self.groups[i]))
            elif i > 10:
                plains.append(PatchCollection(self.groups[i]))
            elif i > 5:
                beach.append(PatchCollection(self.groups[i]))
            elif i > 0:
                water.append(PatchCollection(self.groups[i]))
            else:
                deep.append(PatchCollection(self.groups[i]))

        mountains_colours = ["#FFFFFF","#F4F4F4","#F0F0F0","#E0E0E0","#D0D0D0","#C0C0C0","#B0B0B0","#A0A0A0","#909090","#808080","#707070","#606060","#505050","#404040","#303030","#303030","#303030"]
        mountains_colours = mountains_colours[::-1]
        for count, i in enumerate(mountains):
            ax.add_collection(i)
            i.set_color(mountains_colours[count])

        hills_colours = ["#006600","#006600","#006600","#007600","#007600","#007600","#008600","#008600","#008600","#009600","#009600","#009600","#00A600","#00A600","#00A600"]
        hills_colours = hills_colours[::-1]
        for count, i in enumerate(hills):
            ax.add_collection(i)
            i.set_color(hills_colours[count])

        plains_colours = [["#00AA00"],["#00AA00"],["#00AA00"],["#00AA00"],["#00CC00"],["#00CC00"],["#00CC00"],["#00CC00"],["#00EE00"],["#00EE00"],["#00EE00"],["#00EE00"],["#33FF33"],["#33FF33"],["#33FF33"],["#33FF33"]]
        plains_colours = plains_colours[::-1]
        for count, i in enumerate(plains):
            ax.add_collection(i)
            i.set_color(plains_colours[count])

        beach_colours = [["#FFFF66"],["#FFFF88"],["#FFFF88"],["#FFFFAA"],["#FFFFAA"]]
        for count, i in enumerate(beach):
            ax.add_collection(i)
            i.set_color(beach_colours[count])

        for i in water:
            ax.add_collection(i)
            i.set_color("#00FFFF")

        for i in deep:
            ax.add_collection(i)
            i.set_color("#0000FF")

        self.generate_districts(4)
        self.wall_cells()

        walls = PatchCollection(self.wall_locs)
        ax.add_collection(walls)
        walls.set_color("#000000")

        ax.autoscale_view()
        fig.set_size_inches(10, 10)
        plt.axis("off")
        plt.margins(x=0,y=0) 
        plt.savefig("out_map",bbox_inches='tight')


    def generate_district(self,cell:int,name:str,size:int) -> None:
        for n in self.cell_network.neighbors(cell):
            if (self.cell_network.nodes[n]["ter_type"] == "nat") and (self.cell_network.nodes[n]["district"] == "") and (self.cell_network.nodes[n]["height"] > 5) and (self.cell_network.nodes[n]["height"] < 35):
                self.cell_network.nodes[n]["district"] = name
                if size > 0:
                    self.generate_district(n,name,size-1)
    
    def smooth_districts(self) -> None:
        for cell in self.cell_network.nodes:
            districts = []
            for n in self.cell_network.neighbors(cell):
                districts.append(self.cell_network.nodes[n]["district"])
            if len(set(districts)) == 1:
                self.cell_network.nodes[n]["district"] = districts[0]

    def generate_walls(self) -> None:
        for cell in self.cell_network.nodes:
            if self.cell_network.nodes[cell]["district"] != "":
                for n in self.cell_network.neighbors(cell):
                    if self.cell_network.nodes[n]["district"] == "" and self.cell_network.nodes[n]["ter_type"] == "nat":
                        self.cell_network.nodes[n]["ter_type"] = "wall"


    def generate_districts(self, walls:int) -> None:
        self.walls = walls
        size = (self.walls+1) * 5
        loc = 0
        ## find district location
        random_list = []
        for i, node in enumerate(self.cell_network.nodes):
            random_list.append(node)

        while True:
            loc = random.choice(random_list)
            if (self.cell_network.nodes[loc]["height"] > 5) and (self.cell_network.nodes[loc]["height"] < 35):
                break
        
        self.generate_district(loc,"Center",size)
        self.smooth_districts()

        if self.walls > 0:
            self.generate_walls()

        district_check = 0
        for district in self.districts["inner"]:
            district_check = 1
            info = district.split(":")
            if info[1] == "Residential":
                size = 40*int(info[2])
            elif info[1] == "Industrial":
                size = 10
            elif info[1] == "Commerce":
                size = 30
            elif info[1] == "Religious":
                size = 10
            elif info[1] == "Leisure":
                size = 30
            
            found = 0
            while True:
                loc = random.choice(random_list)
                for n in self.cell_network.neighbors(loc):
                    if (self.cell_network.nodes[n]["ter_type"] == "wall") and (self.cell_network.nodes[loc]["district"] == "") and (self.cell_network.nodes[loc]["height"] > 5) and (self.cell_network.nodes[loc]["height"] < 35):
                        found = 1
                if found == 1:
                    break

            self.generate_district(loc,info[0],size)
            self.smooth_districts()

        if district_check == 1:
            self.generate_walls()

    ########################

        district_check = 0
        for district in self.districts["outer"]:
            district_check = 1
            info = district.split(":")
            if info[1] == "Residential":
                size = 20*int(info[2])
            elif info[1] == "Industrial":
                size = 20
            elif info[1] == "Commerce":
                size = 20
            elif info[1] == "Religious":
                size = 5
            elif info[1] == "Leisure":
                size = 20
            
            found = 0
            while True:
                loc = random.choice(random_list)
                for n in self.cell_network.neighbors(loc):
                    if (self.cell_network.nodes[n]["ter_type"] == "wall") and (self.cell_network.nodes[loc]["district"] == "") and (self.cell_network.nodes[loc]["height"] > 5) and (self.cell_network.nodes[loc]["height"] < 35):
                        found = 1
                if found == 1:
                    break

            self.generate_district(loc,info[0],size)
            self.smooth_districts()

        if district_check == 1:
            self.generate_walls()
        
    ########

        district_check = 0
        for district in self.districts["slums"]:
            district_check = 1
            info = district.split(":")
            if info[1] == "Residential":
                size = 5*int(info[2])
            elif info[1] == "Industrial":
                size = 50
            elif info[1] == "Commerce":
                size = 20
            elif info[1] == "Religious":
                size = 5
            elif info[1] == "Leisure":
                size = 3
            
            found = 0
            while True:
                loc = random.choice(random_list)
                for n in self.cell_network.neighbors(loc):
                    if (self.cell_network.nodes[n]["ter_type"] == "wall") and (self.cell_network.nodes[loc]["district"] == "") and (self.cell_network.nodes[loc]["height"] > 5) and (self.cell_network.nodes[loc]["height"] < 35):
                        found = 1
                if found == 1:
                    break

            self.generate_district(loc,info[0],size)
            self.smooth_districts()

        if district_check == 1:
            self.generate_walls()
        

    def wall_cells(self) -> None:
        self.wall_locs = []
        for i in self.cell_network.nodes:
            ter_type = self.cell_network.nodes[i]["ter_type"]
            if (self.check(self.poly_map.vertices[self.poly_map.regions[i]])) and ter_type == "wall":
                    self.wall_locs.append(Polygon(self.poly_map.vertices[self.poly_map.regions[i]]))

    def show_districts(self) -> None:
        groups = {}

        for i in self.cell_network.nodes:
            district = self.cell_network.nodes[i]["district"]
            if(self.check(self.poly_map.vertices[self.poly_map.regions[i]])):
                if district in groups:
                    groups[district].append(Polygon(self.poly_map.vertices[self.poly_map.regions[i]]))
                else:
                    groups[district] = [Polygon(self.poly_map.vertices[self.poly_map.regions[i]])]

        groups = collections.OrderedDict(sorted(groups.items()))
        


a = poly_map(200,"doom")
a.generate_terain(40,-5,30,30)
a.districts = {"inner":["houses:Residential:5","whouses:Residential:3"],"outer":["houses:Residential:13","houses:Residential:3","houses:Residential:3"],"slums":["houses:Residential:50","houses:Residential:20","houses:Residential:3"]}
a.map_output_elevation()
a.generate_districts(0)



