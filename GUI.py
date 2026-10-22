import math
from tkinter import *


class GUI:
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = Tk()
        self.root.title('Sphere Lighting Simulation')

        self.scene = ''


        self.visualize_update = False
        self.drawing = False

        #canvas dimensions
        self.width = 800
        self.height = 800
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.bind('<Button-1>', self.click)

        #labels, buttons, etc. user input===============================
        self.light_position_label = Label(self.root, text=f'Light Position: ({self.simulation.light.x:.2f}, {self.simulation.light.y:.2f}, {self.simulation.light.z:.2f})')
        self.light_position_label.pack()

        self.step_count_x_entry_field = Entry(self.root)
        self.step_count_x_entry_field.insert(0, self.simulation.step_count_x)

        self.step_count_y_entry_field = Entry(self.root)
        self.step_count_y_entry_field.insert(0,self.simulation.step_count_y)
        self.radius_entry_field = Entry(self.root)
        self.radius_entry_field.insert(0, self.simulation.sphere.radius)
        
        self.step_count_x_entry_description = Label(self.root, text='↑X step count↑')
        self.step_count_y_entry_description = Label(self.root, text='↑Y step count↑')
        self.radius_entry_description = Label(self.root, text='↑Sphere radius↑')

        self.submit_button = Button(self.root, text='Submit', command = self.submit)
        self.export_button = Button(self.root, text='Export', command = self.export)
        self.visualize_update_button = Button(self.root, text='Update Visualization', command = self.visualize_update_switch, bg = 'red')
        
        #=============================================================

        self.step_count_x_entry_field.pack()
        self.step_count_x_entry_description.pack()
        self.step_count_y_entry_field.pack()
        self.step_count_y_entry_description.pack()
        self.radius_entry_field.pack()
        self.radius_entry_description.pack()
        self.submit_button.pack()
        self.export_button.pack()
        self.visualize_update_button.pack()
        self.canvas.pack()

        self.update_canvas()
        
        self.root.mainloop()

        
    #submits the user input at the top of the screen and checks if it is valid. Then updates canvas
    def submit(self):
        step_count_x = 100
        step_count_y = 100
        radius = 5.0
        try:
            step_count_x = int(max(2, min(self.width, int(self.step_count_x_entry_field.get()))))
            step_count_y = int(max(2, min(self.height, int(self.step_count_y_entry_field.get()))))
            radius = max(0.1, min(1000000.0, float(self.radius_entry_field.get())))
        except:
            print('Invalid input. Using default values.')

        self.simulation.step_count_x = step_count_x
        self.simulation.step_count_y = step_count_y
        self.simulation.sphere.radius = radius

        self.simulation.light.x = 0
        self.simulation.light.y = 0
        self.simulation.light.z = self.simulation.sphere.get_z_by_coordinates(0, 0)

        self.update_canvas()


    def export(self):
        with open('scene.txt', 'w') as f:
            f.write(self.scene)

    #switches update visualization on and off
    def visualize_update_switch(self):
        if self.visualize_update_button.cget('bg') == 'red':
            self.visualize_update_button.configure(bg ='green')
            self.visualize_update = True
        else:
            self.visualize_update_button.configure(bg ='red')
            self.visualize_update = False
        
    #determines resolution of the canvas and color of each pixel. Finally draws the pixel
    def update_canvas(self):
        self.drawing = True
        self.scene = self.simulation.run()
        lines = self.scene.splitlines()

        resolution_x = self.width/len(lines[0])
        resolution_y = self.height/len(lines)

        self.canvas.delete('all')

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                x = j * resolution_x
                y = i * resolution_y

                color = '#000000'

                if lines[i][j] == 'S':
                    color = '#000000'
                elif lines[i][j] == 'M':
                    color = '#2D2D2D'
                elif lines[i][j] == '*':
                    color = '#5C5C5C'
                elif lines[i][j] == '+':
                    color = '#868686'
                elif lines[i][j] == '-':
                    color = '#A9A9A9'
                elif lines[i][j] == '.':
                    color = '#D3D3D3'
                elif lines[i][j] == ' ':
                    color = '#FFFFFF'

                self.canvas.create_rectangle(x, y, x + max(1,resolution_x)+1, y + max(1,resolution_y)+1, fill=color, outline=color)

                if self.visualize_update:
                    self.canvas.update()

                
        self.light_position_label.config(text=f'Light Position: ({self.simulation.light.x:.2f}, {self.simulation.light.y:.2f}, {self.simulation.light.z:.2f})')
        self.drawing = False


        
    #mouse position and coordinate mapping
    def click(self, event):
        
        if not self.drawing:
            #get position in coordinates

            mouse_x = event.x
            mouse_y = event.y

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
        