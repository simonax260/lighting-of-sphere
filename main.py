import math
from GUI import GUI
from objects import sphere, light


class simulation:
    def __init__(self, sphere, light, step_count_x, step_count_y):
        self.sphere = sphere
        self.light = light
        self.step_count_x = step_count_x
        self.step_count_y = step_count_y
        self.margin = 1.5

        self.gui = GUI(self)
    
    
    def run(self):


        scene = ''


        #this loop iterates through the grid and uses calculations to determine the light intensity at each point
        for i in range(self.step_count_y):
            for j in range(self.step_count_x):
                x = (self.sphere.radius*self.margin * (2*j / (self.step_count_x - 1) -1)) #maps grid to -1 to 1 range then scales to radius * margin
                y = (self.sphere.radius*self.margin * (2*i / (self.step_count_y - 1) -1)) 
                z = self.sphere.get_z_by_coordinates(x, y)
                intensity = self.light.get_intensity(x, y, z, self.sphere.radius)
                

                
                # Code inspired by Markus Jarderot on https://stackoverflow.com/questions/5883169/intersection-between-a-line-and-a-sphere

                # x(t) = x + light.x * t
                # y(t) = y + light.y * t
                # z(t) = z + light.z * t

                # x(t)^2 + y(t)^2 + z(t)^2 = r^2 formula for line distance from sphere center
                

                # solving for t gives us the following quadratic equation:
                
                if(z == -1):
                    z = 0 #correcting z to 0 if the point is outside the sphere, so that the shadow calculation can be done

                    solution1, solution2 = -1, -1 #t1 and t2

                    #if root is negative, no real solutions exists
                    if (x*light.x + y*light.y + z*light.z)**2 - (light.x**2 + light.y**2 + light.z**2)*(x**2 + y**2 + z**2 - self.sphere.radius**2) >= 0:
                        solution1 = (-(x*light.x + y*light.y + z*light.z) + math.sqrt((x*light.x + y*light.y + z*light.z)**2 - (light.x**2 + light.y**2 + light.z**2)*(x**2 + y**2 + z**2 - self.sphere.radius**2)))/(light.x**2 + light.y**2 + light.z**2)
                        solution2 = (-(x*light.x + y*light.y + z*light.z) - math.sqrt((x*light.x + y*light.y + z*light.z)**2 - (light.x**2 + light.y**2 + light.z**2)*(x**2 + y**2 + z**2 - self.sphere.radius**2)))/(light.x**2 + light.y**2 + light.z**2)


                    if(solution1>0 or solution2>0):
                        #Positive real solutions exists, meaning point is in shadow
                        intensity = -1
                    else:
                        intensity = 0
                
                #End of inspired code


                #Using the intensity to determinte the character displayed
                if intensity == -1:
                    scene += 'S'
                elif intensity <= 0:
                    scene += 'M'
                elif intensity <= 0.3:
                    scene += '*'
                elif intensity <= 0.5:
                    scene += '+'
                elif intensity <= 0.7:
                    scene += '-'
                elif intensity <= 0.9:
                    scene += '.'
                else:
                    scene += ' '
            scene += '\n'

        scene.removesuffix('\n')

        
        return scene

        



        
                
#    
#print('Input radius of the sphere:', end=' ')
#radius = float(input())
#sphere = sphere(radius)
#
#while True:
#
#    print('Input x coordinate of the light source:', end=' ')
#    x = float(input())
#    print('Input y coordinate of the light source:', end=' ')
#    y = float(input())
#    z = sphere.get_z_by_coordinates(x, y)
#
#    if z == -1:
#        print('The light source is outside the sphere. Please enter valid coordinates.', end=' ')
#        continue
#    else:
#        break
#
#light = light(x, y, z)

sphere = sphere(5.0)
light = light(0, 0, sphere.get_z_by_coordinates(0, 0))
step_count_x = 100
step_count_y = 100

simulation = simulation(sphere, light, step_count_x, step_count_y)
