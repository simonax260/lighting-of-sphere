
import math


class sphere:
    def __init__(self, radius):
        self.radius = radius
    
    def get_z_by_coordinates(self, x,y):
        if x**2 + y**2 <= self.radius**2:
            z = math.sqrt(round(self.radius**2 - x**2 - y**2, 5)) #rounding to avoid floating point errors
            return z
        else:
            return -1



class light:
    def __init__(self, x,y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot_product(self, x,y, z):
        return self.x * x + self.y * y + self.z * z

    def get_intensity(self, x,y,z, r):
        dot = self.dot_product(x,y,z)
        intensity = dot/(r**2)
        return intensity

