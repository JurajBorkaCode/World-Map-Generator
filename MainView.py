import tkinter
import tkinter.messagebox
import customtkinter

import startUp
import town
import os
from PIL import Image

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Map Maker")
        self.geometry(f"{1700}x{900}")
        self.state("zoomed")

        start_up = startUp.StartUp(self, self.winfo_x(), self.winfo_y())

        start_up_data = start_up.get_input()

        if start_up_data == "World":
            self.create_world()
        elif start_up_data == "Region":
            self.create_region()
        elif start_up_data == "Town":
            self.create_town()
        elif start_up_data == "Dungeon":
            self.create_dungeon()




    def create_world(self):
        pass

    def create_region(self):
        pass

    def create_dungeon(self):
        pass
        



    #### town functions

    def create_town(self):
        self.town = town.Town()

        self.options_frame = customtkinter.CTkFrame(self, width=500, corner_radius=0)
        self.options_frame.pack(side = tkinter.LEFT, fill = tkinter.Y)

        self.display_frame = customtkinter.CTkFrame(self, width=1410, corner_radius=0)
        self.display_frame.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        size = tkinter.IntVar(value=0)     
        walls = tkinter.IntVar(value=0)

        self.dis_name = tkinter.StringVar(value="District Name")
        self.dis_type = "Residential"
        self.dis_size = tkinter.StringVar(value="District Pop Size")

        self.size_walls_frame = customtkinter.CTkFrame(self.options_frame, width=500, corner_radius=0)
        self.size_walls_frame.pack(side = tkinter.TOP, fill = tkinter.Y)


        self.logo_label = customtkinter.CTkLabel(self.size_walls_frame, text="Creation Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.size_label = customtkinter.CTkLabel(self.size_walls_frame, text="Town size:", anchor="w")
        self.size_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.size_combo = customtkinter.CTkComboBox(self.size_walls_frame, values=["1", "2", "3"],command=self.change_town_size)
        self.size_combo.grid(row=1, column=1, padx=20, pady=(10, 10))

        self.walls_label = customtkinter.CTkLabel(self.size_walls_frame, text="Number of walls between town center and wild:", anchor="w")
        self.walls_label.grid(row=2, column=0, padx=10, pady=(10, 10))
        self.walls_combo = customtkinter.CTkComboBox(self.size_walls_frame, values=["0","1", "2", "3"],command=self.change_town_walls)
        self.walls_combo.grid(row=2, column=1, padx=10, pady=(10, 10))
        
        self.districts = customtkinter.CTkTabview(self.options_frame, width=450, height=500)
        self.districts.pack(side = tkinter.TOP, fill = tkinter.Y)
        self.districts.add("Center")
        self.districts.tab("Center").grid_columnconfigure(0, weight=1)

        self.districts_description = customtkinter.CTkLabel(self.districts.tab("Center"), text="This is the Districts menu.\nThe Center district will contain buildings based on the amount of walls.\n0 - Village Hall\n1 - Town Hall, Tax Office\n2 - Town Hall, Tax Office, Bank\n3 - City Hall, Tax Office, Bank, Temple\n\nDistricts have different types.\nResidential - Housing\nIndustrial - Production\nCommerce - Shops and Restaurants\nReligious - Churches and Temples\nLeisure - Parks, Theaters, and Colleseums", anchor="w")
        self.districts_description.grid(row=0, column=0, padx=20, pady=(10, 10))
        dis_Help = customtkinter.CTkButton(self.districts.tab("Center"), command=self.district_help, text= "Help", font=("Arial", 15),width=50)
        dis_Help.grid(row=1, column=0, padx=20, pady=(10, 10))


        self.districts_mod_frame = customtkinter.CTkFrame(self.options_frame, width=500, corner_radius=0)
        self.districts_mod_frame.pack(side = tkinter.TOP, fill = tkinter.Y)

        self.district_name_to_add = customtkinter.CTkEntry(self.districts_mod_frame, width= 120, placeholder_text="Distric Name", textvariable=self.dis_name)
        self.district_name_to_add.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew")

        self.district_type_to_add = customtkinter.CTkComboBox(self.districts_mod_frame, width= 120, values=["Residential","Industrial","Commerce","Religious","Leisure"],command=self.dis_type_get)
        self.district_type_to_add.grid(row=0, column=1, padx=(10, 0), pady=(10, 10), sticky="nsew")

        self.district_size_to_add = customtkinter.CTkEntry(self.districts_mod_frame, width= 120, placeholder_text="Distric Population Size", textvariable=self.dis_size)
        self.district_size_to_add.grid(row=0, column=2, padx=(10, 0), pady=(10, 10), sticky="nsew")

        dis_add = customtkinter.CTkButton(self.districts_mod_frame, command=self.add_district, text= "Add", font=("Arial", 15),width=50)
        dis_add.grid(row=0, column=3, padx=(10, 0), pady=(10, 10), sticky="nsew")

        self.other_options_frame = customtkinter.CTkFrame(self.options_frame, width=500, corner_radius=0)
        self.other_options_frame.pack(side = tkinter.TOP, fill = tkinter.Y)

        self.river = customtkinter.CTkCheckBox(self.other_options_frame,text="River")
        self.river.grid(row=0, column=0, pady=10, padx=20, sticky="n")

        self.seed = tkinter.StringVar(value=None)
        self.custom_seed = customtkinter.CTkEntry(self.other_options_frame, textvariable=self.seed)
        self.custom_seed.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.seed_label = customtkinter.CTkLabel(self.other_options_frame, text="Seed:", anchor="w")
        self.seed_label.grid(row=1, column=0, padx=20, pady=(10, 0))

        gen_btn = customtkinter.CTkButton(self.other_options_frame, command=self.generate_map, text= "Generate Map", font=("Arial", 15),width=150)
        gen_btn.grid(row=5, column=0, padx=20, pady=(10, 10))


    def generate_map(self):
        print(self.river.get())
        self.town.generate_map(self.seed.get(),river=self.river.get())
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        self.map_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "map.png")), size=(1000, 1000))
        try:
            self.image_frame.destroy()
        except:
            pass
        self.image_frame = customtkinter.CTkLabel(self.display_frame,image=self.map_image,text="")
        self.image_frame.pack()

    def district_help(self):
        pass


    def add_district(self):
        region = self.districts.get()
        if region != "Center":
            self.walls_combo.configure(state="disabled")
        else:
            return None

        if region == "Slums" and len(self.town.districts["Slums"]) > 7:
            return None
        
        if region == "Outer" and len(self.town.districts["Outer"]) > 5:
            return None

        if region == "Inner" and len(self.town.districts["Inner"]) > 2:
            return None


        if region == "Inner":
            district = customtkinter.CTkFrame(self.inner_frame, width=450, corner_radius=0)
        elif region == "Outer":
            district = customtkinter.CTkFrame(self.outer_frame, width=450, corner_radius=0)
        else:
            district = customtkinter.CTkFrame(self.slums_frame, width=450, corner_radius=0)
        district.pack(side = tkinter.TOP)

        if self.dis_name.get() == "District Name":
            d_name = customtkinter.CTkLabel(district, text=f"Distric name: District {len(self.town.districts[region]) + 1}", anchor="w")
        else:
            d_name = customtkinter.CTkLabel(district, text=f"Distric name: {self.dis_name.get()}", anchor="w")
        d_name.grid(row=0, column=0, padx=10, pady=(10, 10))

        d_type = customtkinter.CTkLabel(district, text=f"Distric type: {self.dis_type}", anchor="w")
        d_type.grid(row=0, column=1, padx=10, pady=(10, 10))

        if self.dis_size.get() == "District Pop Size":
            d_size = customtkinter.CTkLabel(district, text=f"Distric size: 0", anchor="w")
        else:
            d_size = customtkinter.CTkLabel(district, text=f"Distric size: {self.dis_size.get()}", anchor="w")
        d_size.grid(row=0, column=2, padx=10, pady=(10, 10))

        self.town.add_district(region,self.dis_name.get(),self.dis_type,self.dis_size.get())

    def dis_type_get(self, new_type: str):
        self.dis_type = new_type

    def change_town_size(self, new_size: str):
        self.town.set_size(new_size)

    def change_town_walls(self, new_walls: str):
        self.town.walls = new_walls
        self.districts_mod(new_walls)

    def districts_mod(self,walls):
        try:
            self.districts.delete("Slums")
            self.districts.delete("Outer")
            self.districts.delete("Inner")
        except:
            pass
        if walls == "0":
            return None
        if walls == "1":
            self.districts.add("Slums")
            self.districts.tab("Slums").grid_columnconfigure(0, weight=1)
            self.slums_frame = customtkinter.CTkFrame(self.districts.tab("Slums"), width=420, corner_radius=0)
            self.slums_frame.grid(row=0, column=0)
        elif walls == "2":
            self.districts.add("Outer")
            self.districts.tab("Outer").grid_columnconfigure(0, weight=1)
            self.districts.add("Slums")
            self.districts.tab("Slums").grid_columnconfigure(0, weight=1)
            self.outer_frame = customtkinter.CTkFrame(self.districts.tab("Outer"), width=420, corner_radius=0)
            self.outer_frame.grid(row=0, column=0)
            self.slums_frame = customtkinter.CTkFrame(self.districts.tab("Slums"), width=420, corner_radius=0)
            self.slums_frame.grid(row=0, column=0)
        elif walls == "3":
            self.districts.add("Inner")
            self.districts.tab("Inner").grid_columnconfigure(0, weight=1)
            self.districts.add("Outer")
            self.districts.tab("Outer").grid_columnconfigure(0, weight=1)
            self.districts.add("Slums")
            self.districts.tab("Slums").grid_columnconfigure(0, weight=1)
            self.inner_frame = customtkinter.CTkFrame(self.districts.tab("Inner"), width=420, corner_radius=0)
            self.inner_frame.grid(row=0, column=0)
            self.outer_frame = customtkinter.CTkFrame(self.districts.tab("Outer"), width=420, corner_radius=0)
            self.outer_frame.grid(row=0, column=0)
            self.slums_frame = customtkinter.CTkFrame(self.districts.tab("Slums"), width=420, corner_radius=0)
            self.slums_frame.grid(row=0, column=0)

    