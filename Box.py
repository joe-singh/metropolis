"""Box Class"""
import numpy as np
from Particle import Particle

class Box:

    def __init__(self, width, height, particles=[]):
        self.width = width
        self.height = height
        self.particles = particles

    def get_config_energy(self):
        energy = 0
        for i in range(len(self.particles)-1):
            for j in range(i+1, len(self.particles)):
                energy += calculate_particle_energy(self.particles[i], self.particles[j])
        return energy

    def get_x_array(self):
        return np.array([particle.get_x() for particle in self.particles])

    def get_y_array(self):
        return np.array([particle.get_y() for particle in self.particles])

"""Defines how to calculate energy"""
def calculate_particle_energy(particle_1, particle_2):
    x_1 = particle_1.get_x()
    x_2 = particle_2.get_x()
    y_1 = particle_1.get_y()
    y_2 = particle_2.get_y()

    return 1/(((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** .5)
