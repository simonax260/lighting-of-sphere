from tkinter import *
from turtle import width


class GUI:
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = Tk()
        self.root.title("Sphere Lighting Simulation")

        self.width = 800
        self.height = 800
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.bind("<Button-1>", self.click)

        self.light_position_label = Label(self.root, text=f"Light Position: ({self.simulation.light.x:.2f}, {self.simulation.light.y:.2f}, {self.simulation.light.z:.2f})")
        self.light_position_label.pack()

        self.step_count_x_text_field = Text(self.root)
        self.step_count_x_text_field.pack()
        
        self.canvas.pack()
        self.root.mainloop()

    def update_canvas(self):
        lines = self.simulation.run().splitlines()

        resolution_x = self.width/len(lines[0])
        resolution_y = self.height/len(lines)

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                x = j * resolution_x
                y = i * resolution_y

                color = '#000000'

                if lines[i][j] == 'S':
                    color = "#000000"
                elif lines[i][j] == 'M':
                    color = "#2D2D2D"
                elif lines[i][j] == '*':
                    color = "#5C5C5C"
                elif lines[i][j] == '+':
                    color = "#868686"
                elif lines[i][j] == '-':
                    color = "#A9A9A9"
                elif lines[i][j] == '.':
                    color = "#D3D3D3"
                elif lines[i][j] == ' ':
                    color = "#FFFFFF"

                self.canvas.create_rectangle(x, y, x + resolution_x, y + resolution_y, fill=color)

                
        self.light_position_label.config(text=f"Light Position: ({self.simulation.light.x:.2f}, {self.simulation.light.y:.2f}, {self.simulation.light.z:.2f})")



        

    def click(self, event):
        

        #get position in coordinates

        mouse_x = event.x
        mouse_y = event.y
        print(mouse_x, mouse_y)

        x_range = self.simulation.sphere.radius * self.simulation.margin
        y_range = self.simulation.sphere.radius * self.simulation.margin

        x = (mouse_x / self.width) * 2 * x_range - x_range
        y = (mouse_y / self.height) * 2 * y_range - y_range
        z = self.simulation.sphere.get_z_by_coordinates(x, y)

        if z != -1:
            self.simulation.light.x = x
            self.simulation.light.y = y
            self.simulation.light.z = z


        self.update_canvas()