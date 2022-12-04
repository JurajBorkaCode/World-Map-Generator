from PIL import Image
import numpy
import scipy.signal
import math

import random
import townMapCell

class generated_map():
    def __init__(self,x,y,topo="mountains",seed=None):
        self.x = x
        self.y = y
        self.seed = random.seed(a=seed)
        self.height_max = 4
        self.height_min = 1
        if topo == "plains":
            self.height_max = 4
            self.height_min = 1
        elif topo == "hills":
            self.height_max = 7
            self.height_min = 2
        elif topo == "mountains":
            self.height_max = 10
            self.height_min = 5
        self.values = [[townMapCell.Cell(height=self.height_min) for i in range(x)] for j in range(y)]
        self.map_image = Image.new('RGB',(self.x,self.y), (255, 255, 255))

    def create_map_image(self,style="standard",name = "image"):

        for x in range(self.x):
            for y in range(self.y):
                self.values[x][y].height = self.smooth(x,y,self.values[x][y].height)
                self.values[x][y].g_type = self.smooth_river(x,y,self.values[x][y].g_type)
                self.values[x][y].g_type = self.smooth_river(x,y,self.values[x][y].g_type)


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


        #self.map_image.putpixel((500,500),(255, 0, 0))
        self.map_image.save(name+".png", "PNG")

    def create_topography_map(self):
        random_val_list = list(range(self.height_min,self.height_max)) + [self.height_min] * 100 + [self.height_max] * 40
        for x in range(self.x):
            for y in range(self.y):
                self.values[x][y].height = random.choice(random_val_list)
    

    def generate_river(self):
        river_x = self.x-1
        river_y = self.y-1
        

        if random.randint(1,2) == 1:
            river_x = random.randint(0,self.x-1)
        else:
            river_y = random.randint(0,self.y -1)

        self.values[river_x][river_y].g_type = "water"
        self.values[river_x][river_y].height = self.height_max

        if self.x == 100:
            size_adj = 100
        if self.x == 500:
            size_adj = 2000
        elif self.x == 1000:
            size_adj = 2000
        elif self.x == 3000:
            size_adj = 10000
        


        for i in range(self.x*size_adj):
            self.values[river_x][river_y].g_type = "water"
            self.values[river_x][river_y].height = self.height_max
            try:
                if self.values[river_x+1][river_y].height == self.height_min:
                    river_x += 1
                    continue
            except:
                pass

            try:
                if self.values[river_x-1][river_y].height == self.height_min:
                    river_x -= 1
                    continue
            except:
                pass

            try:
                if self.values[river_x][river_y+1].height == self.height_min:
                    river_y += 1
                    continue
            except:
                pass

            try:
                if self.values[river_x][river_y-1].height == self.height_min:
                    river_y -= 1
                    continue
            except:
                pass

            while True:
                rand_dir = random.randint(1,4)
                if rand_dir == 1 and river_x < self.x - 1:
                    river_x += 1
                    break
                elif rand_dir == 2 and river_x > 0:
                    river_x -= 1
                    break
                elif rand_dir == 3 and river_y < self.y - 1:
                    river_y += 1
                    break
                elif rand_dir == 4 and river_y > 0:
                    river_y -= 1
                    break


    def gaussian_blur_river(self):
        new_values = [[[] for i in range(self.x)] for i in range(self.y)]
        for x in range(self.x):
            for y in range(self.y):
                if self.values[x][y].g_type == "water":
                    new_values[x][y] = 1
                else:
                    new_values[x][y] = 0
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
                t_vals = {0:"land",1:"water"}
                if out_val < 0:
                    out_val = 0
                elif out_val > 1:
                    out_val = 1
                self.values[x][y].g_type = t_vals[out_val]
                    




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
                    self.values[x][y].height = random.choice(list(range(self.height_min,self.height_max)) + [self.height_min] * 100 + [self.height_max] * 40)
                elif out_val > self.height_max:
                    self.values[x][y].height = self.height_max

    def smooth(self,x,y,current_height):
        try:
            if (self.values[x+1][y].height == self.values[x-1][y].height == self.values[x][y+1].height == self.values[x][y-1].height) or (self.values[x+1][y].height == self.values[x-1][y].height):
                return self.values[x+1][y].height
            elif (self.values[x][y+1].height == self.values[x][y-1].height):
                return self.values[x][y+1].height
            else:
                return current_height
        except:
            return current_height

    def smooth_river(self,x,y,current_t_type):
        try:
            if (self.values[x+1][y].g_type == self.values[x-1][y].g_type == self.values[x][y+1].g_type == self.values[x][y-1].g_type) or (self.values[x+1][y].g_type == self.values[x-1][y].g_type):
                return self.values[x+1][y].g_type
            elif (self.values[x][y+1].g_type == self.values[x][y-1].g_type):
                return self.values[x][y+1].g_type
            else:
                return current_t_type
        except:
            return current_t_type




    