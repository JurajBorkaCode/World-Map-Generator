class Town():
    def __init__(self):
        self.size = 0
        self.pop = 0
        self.walls = 0
        self.x = 0
        self.y = 0
        self.districts = {"Inner":[],"Outer":[],"Slums":[]}
        self.coast = 0
        self.river = 0
        self.wealth = 0
        self.gates = 0


    def add_district(self,location,name,d_type,population):
        self.districts[location].append((name,d_type,population))

    def set_size(self, size): #1=500x500, 2= 1000x1000, 3=2000x2000
        if size == "1":
            self.x = 500
            self.y = 500
        elif size == "2":
            self.x = 1000
            self.y = 1000
        elif size == "3":
            self.x = 3000
            self.y = 3000
