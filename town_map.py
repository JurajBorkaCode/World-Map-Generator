from PIL import Image
import random
import townMapCell
import copy
import numpy
import scipy
import math

class Town_Map:
    def __init__(self,x:int,y:int,topo:str="mountains",seed:str=None):
        self.x = x
        self.y = y
        if topo == "plains":
            self.height_max = 4
            self.height_min = 1
        elif topo == "hills":
            self.height_max = 7
            self.height_min = 2
        elif topo == "mountains":
            self.height_max = 10
            self.height_min = 5
        
        if seed is not None:
            random.seed(seed)

        self.values = [[townMapCell.Cell(height=self.height_min) for i in range(x)] for j in range(y)]
        self.map_image = Image.new('RGB',(self.x,self.y), (255, 255, 255))

    def create_map(self,name:str,style:str="topo"):
        
        if style == "topo":
            topo_colours = {1:(200, 255, 0),2:(255, 255, 0),3:(255, 220, 0),4:(255, 190, 0),5:(255, 160, 0),6:(255, 130, 0),7:(255, 100, 0),8:(255, 70, 0),9:(255, 40, 0),10:(255, 10, 0)}
            for x in range(self.x):
                for y in range(self.y):
                    if self.values[x][y].height != 0:
                        self.map_image.putpixel((x,y),topo_colours[self.values[x][y].height])
        elif style == "standard":
            pass

        for x in range(self.x):
            for y in range(self.y):
                if self.values[x][y].g_type == "water":
                    self.map_image.putpixel((x,y),(0,0,255))
        
        self.map_image.save(name+".png", "PNG")

    def generate_topo(self,peaks:int,times:int):
        for i in range(peaks):
            x = random.randint(0,self.x-1)
            y = random.randint(0,self.y-1)
            self.values[x][y].height = self.height_max
        

        counter = 0
        for i in range(times):
            if counter == int(times/3):
                self.gaussian_blur()
                counter = 0

            new_map = copy.deepcopy(self.values)
            for x in range(self.x):
                for y in range(self.y):
                    if self.values[x][y].height > self.height_min:
                        new_map = self.change_height(x+1,y,self.values[x][y].height,new_map)
                        new_map = self.change_height(x-1,y,self.values[x][y].height,new_map)
                        new_map = self.change_height(x,y+1,self.values[x][y].height,new_map)
                        new_map = self.change_height(x,y-1,self.values[x][y].height,new_map)
            self.values = new_map
            counter += 1
        
        for x in range(self.x):
            for y in range(self.y):
                self.values[x][y].height = self.smooth(x,y,self.values[x][y].height)
                self.values[x][y].height = self.smooth(x,y,self.values[x][y].height)

    def change_height(self,x:int,y:int,new_height:int,new_map:list[list[townMapCell.Cell]]) -> list[list[townMapCell.Cell]]:
        try:
            if self.values[x][y].height < new_height:
                if random.randint(1,100) < 50:
                    new_map[x][y].height = new_height
                else:
                    if self.values[x][y].height != self.height_min:
                        new_map[x][y].height = new_height - 1
        except:
            pass
        return new_map


    def change_g_type(self,x:int,y:int,new_map:list[list[townMapCell.Cell]]) -> list[list[townMapCell.Cell]]:
        try:
            if random.randint(1,100) < 40:
                new_map[x][y].g_type = "water"
        except:
            pass
        return new_map


    def generate_coast(self):
        initial_size = random.randint(int(self.x*0.03),int(self.x*0.05))

        for x in range(self.y):
            for y in range(initial_size):
                self.values[x][y].g_type = "water"
            direction = random.randint(1,3)
            if direction == 1:
                if initial_size < self.x:
                    initial_size += 1
                else:
                    initial_size -= 1
            elif direction == 2:
                if initial_size > 0:
                    initial_size -= 1
                else:
                    initial_size += 1
                

    def gaussian_blur(self):
        new_values = [[[self.height_min] for i in range(self.x)] for i in range(self.y)]
        for x in range(self.x):
            for y in range(self.y):
                new_values[x][y] = self.values[x][y].height
        new_values = numpy.array(new_values)
        convolution_array = numpy.array([
            [0.01875,0.01875,0.01875,0.01875,0.01875],
            [0.01875,0.05,0.05,0.05,0.01875],
            [0.01875,0.05,0.3,0.05,0.01875],
            [0.01875,0.05,0.05,0.05,0.01875],
            [0.01875,0.01875,0.01875,0.01875,0.01875]
        ])



        #convolution_array = numpy.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
        out = scipy.signal.fftconvolve(new_values,convolution_array)
        for x in range(self.x):
            for y in range(self.y):
                out_val = math.ceil(out[x][y])
                self.values[x][y].height = out_val

                if out_val < self.height_min:
                    #self.values[x][y].height = random.choice(list(range(self.height_min,self.height_max)) + [self.height_min] * 100 + [self.height_max] * 10)
                    self.values[x][y].height = self.height_min
                elif out_val > self.height_max:
                    self.values[x][y].height = self.height_max


    def smooth(self,x:int,y:int,current_height:int) -> int:
        try:
            if (self.values[x+1][y].height == self.values[x-1][y].height == self.values[x][y+1].height == self.values[x][y-1].height) or (self.values[x+1][y].height == self.values[x-1][y].height):
                return self.values[x+1][y].height
            elif (self.values[x][y+1].height == self.values[x][y-1].height):
                return self.values[x][y+1].height
            else:
                return current_height
        except:
            return current_height


    def widen_river(self,times:int):
        for i in range(times):
            new_map = copy.deepcopy(self.values)
            for x in range(self.x):
                for y in range(self.y):
                    if self.values[x][y].g_type == "water":
                        new_map = self.change_g_type(x+1,y,new_map)
                        new_map = self.change_g_type(x-1,y,new_map)
                        new_map = self.change_g_type(x,y+1,new_map)
                        new_map = self.change_g_type(x,y-1,new_map)
            self.values = new_map


    def create_river(self,direction:int):
        river_x = 0
        river_y = 0
        if direction == 1:  # get start location of the river
            river_x = random.randint(0,self.x)
        else:
            river_y = random.randint(0,self.y)

        while True:
            try:
                self.values[river_x][river_y].g_type = "water"
                self.flood_fill(river_x,river_y)
            except:
                pass

            if direction == 1:
                if river_y == self.y:
                    break

                if random.randint(0,100) < 50:
                    river_y += 1
                else:
                    if random.randint(1,2) == 1:
                        river_x +=1
                    else:
                        river_x -=1
            else:
                if river_x == self.x:
                    break

                if random.randint(0,100) < 50:
                    river_x += 1
                else:
                    if random.randint(1,2) == 1:
                        river_y +=1
                    else:
                        river_y -=1


    def gaussian_water(self):
        new_values = [[0 for i in range(self.x)] for i in range(self.y)]
        for x in range(self.x):
            for y in range(self.y):
                if self.values[x][y].g_type == "water":
                    new_values[x][y] = 1
        new_values = numpy.array(new_values)
        convolution_array = numpy.array([
            [0.01875,0.01875,0.01875,0.01875,0.01875],
            [0.01875,0.05,0.05,0.05,0.01875],
            [0.01875,0.05,0.3,0.05,0.01875],
            [0.01875,0.05,0.05,0.05,0.01875],
            [0.01875,0.01875,0.01875,0.01875,0.01875]
        ])



        out = scipy.signal.fftconvolve(new_values,convolution_array)
        for x in range(self.x):
            for y in range(self.y):
                out_val = out[x][y]
                if out_val == 1:
                    self.values[x][y].g_type = "water"
                if out_val > 0.1:
                    self.values[x][y].g_type = "water"


    def flood_fill(self,x:int,y:int):
        if self.values[x][y].height == self.height_min:
            self.values[x][y].g_type = "water"
            self.values[x][y].height = self.height_min - 1
            if x > 0:
                self.flood_fill(x-1,y)
            if x < self.y - 1:
                self.flood_fill(x+1,y)
            if y > 0:
                self.flood_fill(x,y-1)
            if y < self.x - 1:
                self.flood_fill(x,y+1)


    def generate_town_center(self):
        pass

    def get_min_max_hight(self):
        heights = []
        for x in range(self.x):
            for y in range(self.y):
                heights.append(self.values[x][y].height)
        self.height_max = max(heights)
        self.height_min = min(heights)

a = Town_Map(200,200,seed="jjhd",topo="plains")
a.generate_topo(10,30)
a.get_min_max_hight()
a.create_river(1)
a.widen_river(3)
a.gaussian_water()
a.generate_coast()
a.create_map("town_map")