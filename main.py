import math
from unittest import case
from GUI import GUI


class sphere:
    def __init__(self, radius):
        self.radius = radius
    
    def get_z_by_coordinates(self, x,y):
        if x**2 + y**2 <= self.radius**2:
            z = math.sqrt(round(self.radius**2 - x**2 - y**2, 5)) #rounding to avoid floating point errors
            return z
        else:
            return -1
    def get_radius(self):
        return self.radius



class light:
    def __init__(self, x,y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot_product(self, x,y, z):
        return self.x * x + self.y * y + self.z * z

    def get_intensity(self, x,y,z, r):
        dot = self.dot_product(x,y,z)
        b = dot/(r**2)
        return b



class simulation:
    def __init__(self, sphere, light, step_count_x, step_count_y):
        self.sphere = sphere
        self.light = light
        self.step_count_x = step_count_x
        self.step_count_y = step_count_y
        self.margin = 1.2

        self.gui = GUI(self)

    def set_step_count_x(self, step_count_x):
        self.step_count_x = step_count_x
    def set_step_count_y(self, step_count_y):
        self.step_count_y = step_count_y
    
    
    def run(self):


        scene = ''
        


        for i in range(self.step_count_y):
            for j in range(self.step_count_x):
                x = (self.sphere.radius*self.margin * (2*(j / self.step_count_x) - 1))
                y = (self.sphere.radius*self.margin * (2*(i / self.step_count_y) - 1))
                z = self.sphere.get_z_by_coordinates(x, y)
                b = self.light.get_intensity(x, y, z, self.sphere.radius)
                

                
                # Code inspired by Markus Jarderot on https://stackoverflow.com/questions/5883169/intersection-between-a-line-and-a-sphere

                # x(t) = x + light.x * t
                # y(t) = y + light.y * t
                # z(t) = z + light.z * t

                # x(t)^2 + y(t)^2 + z(t)^2 = r^2 formula for line distance from sphere center
                

                # t = (r^2 )

                if(z == -1):
                    z = 0 #correcting z to 0 if the point is outside the sphere, so that the shadow calculation can be done
                    t1, t2 = -1,-1
                    if (x*light.x + y*light.y + z*light.z)**2 - (light.x**2 + light.y**2 + light.z**2)*(x**2 + y**2 + z**2 - self.sphere.radius**2) >= 0:
                        t1 = (-(x*light.x + y*light.y + z*light.z) + math.sqrt((x*light.x + y*light.y + z*light.z)**2 - (light.x**2 + light.y**2 + light.z**2)*(x**2 + y**2 + z**2 - self.sphere.radius**2)))/(light.x**2 + light.y**2 + light.z**2)
                        t2 = (-(x*light.x + y*light.y + z*light.z) - math.sqrt((x*light.x + y*light.y + z*light.z)**2 - (light.x**2 + light.y**2 + light.z**2)*(x**2 + y**2 + z**2 - self.sphere.radius**2)))/(light.x**2 + light.y**2 + light.z**2)


                    if(t1>0 or t2>0):
                        #Confirms that the point intersects with the sphere in the direction of the light source, meaning it is in shadow
                        b = -1
                    else:
                        b = 0
                
                #End of inspired code

                if b == -1:
                    scene += "S"
                elif b <= 0:
                    scene += 'M'
                elif b <= 0.3:
                    scene += '*'
                elif b <= 0.5:
                    scene += '+'
                elif b <= 0.7:
                    scene += '-'
                elif b <= 0.9:
                    scene += '.'
                else:
                    scene += ' '
            scene += '\n'

        scene.removesuffix('\n')

        
        return scene

        



        
                
    
print('Input radius of the sphere:', end=' ')
radius = float(input())
sphere = sphere(radius)

while True:

    print('Input x coordinate of the light source:', end=' ')
    x = float(input())
    print('Input y coordinate of the light source:', end=' ')
    y = float(input())
    z = sphere.get_z_by_coordinates(x, y)

    if z == -1:
        print('The light source is outside the sphere. Please enter valid coordinates.', end=' ')
        continue
    else:
        break

light = light(x, y, z)

step_count_x = 100
step_count_y = 100

simulation = simulation(sphere, light, step_count_x, step_count_y)
simulation.run()
