import tkinter
import tkinter.messagebox
import customtkinter

class StartUp(customtkinter.CTkToplevel):
    def __init__(self,parent,x,y):
        super().__init__(parent)

        self.submit = False
        self.selection = None

        self.title("Map Maker")
        self.lift()  # lift window on top
        self.attributes("-topmost", True)
        self.after(10, self._create_widgets)
        self.resizable(False, False)
        self.grab_set()
        self.geometry('%dx%d+%d+%d' % (300, 250, x+900, y+100))
        

    def _create_widgets(self):
        load_map = customtkinter.CTkButton(master=self, command=self.load_map, text= "Load Map", font=("Arial", 25))
        load_map.pack(pady=5, padx=10, fill='both', expand=True)

        world_map = customtkinter.CTkButton(master=self, command=self.create_world_map, text= "Create world map", font=("Arial", 25))
        world_map.pack(pady=5, padx=10, fill='both', expand=True)

        region_map = customtkinter.CTkButton(master=self, command=self.create_region_map, text= "Create region map", font=("Arial", 25))
        region_map.pack(pady=5, padx=10, fill='both', expand=True)

        town_map = customtkinter.CTkButton(master=self, command=self.create_town_map, text= "Create town map", font=("Arial", 25))
        town_map.pack(pady=5, padx=10, fill='both', expand=True)

        dungeon_map = customtkinter.CTkButton(master=self, command=self.create_dungeon_map, text= "Create dungeon map", font=("Arial", 25))
        dungeon_map.pack(pady=5, padx=10, fill='both', expand=True)

    def load_map(self):
        pass

    def create_world_map(self):
        self.selection_complete("World")

    def create_region_map(self):
        self.selection_complete("Region")

    def create_town_map(self):
        self.selection_complete("Town")

    def create_dungeon_map(self):
        self.selection_complete("Dungeon")

    def selection_complete(self,par):
        self.selection = par
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self.selection