"""Metropolis Algorithm simulation
    By Joe Singh 11/6/18 
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Box import Box
from Particle import Particle

# Boltzmann Constant
k = 1.38e-23

"""Checks if particle is within the boundaries of the box"""
def meets_box_boundary_condition(box, x, y):
    return x <= box.width and y <= box.height and x >= 0 and y >= 0

"""Checks if particle is within circular boundary in circle defined by
   (x - xc)^2 + (y - yc)^2 = r^2 """
def meets_circular_boundary_condition(x, y, r, xc, yc):
    return not (x - xc) ** 2 + (y - yc) ** 2 > r**2

"""Applies the metropolis algorithm to update particle positions in box"""
def metropolis(frames, box, temp, num_particles, points):

    # Alpha parameter limits max motion of particles during algorithm so we don't simulate
    # particles teleporting from one place to another. Set to 1/100 of the average of
    # the box's dimensions
    print(frames)
    alpha = ((box.height + box.width)/2)/10

    # Pick a particle at random
    rand_index = np.random.randint(0, num_particles)
    rand_particle = box.particles[rand_index]

    # Store current information before any movement
    old_x = rand_particle.get_x()
    old_y = rand_particle.get_y()
    old_energy = box.get_config_energy()

    delta_x = np.random.uniform(-alpha, alpha)
    delta_y = np.random.uniform(-alpha, alpha)

    new_x = old_x + delta_x
    new_y = old_y + delta_y

    # If generated position not valid, reset particle position and end metropolis step.

    if not meets_box_boundary_condition(box, new_x, new_y):
        rand_particle.set_x(old_x)
        rand_particle.set_y(old_y)
        points.set_xdata(box.get_x_array())
        points.set_ydata(box.get_y_array())
        return box.get_x_array(),

    # Move particle, get new configuration energy
    rand_particle.set_x(old_x + delta_x)
    rand_particle.set_y(old_y + delta_y)
    new_energy = box.get_config_energy()

    if np.random.random() > min(1, np.exp(-(new_energy - old_energy)/(k * temp))):
        # If Metropolis criteria not met return to original position and start again
        rand_particle.set_x(old_x)
        rand_particle.set_y(old_y)

    points.set_xdata(box.get_x_array())
    points.set_ydata(box.get_y_array())
    return box.get_x_array(),


"""Main method runs everything and creates animation"""
def run(num_particles, box_width, box_height, temp, num_steps):
    fig, ax = plt.subplots()

    particle_array = []
    for i in range(num_particles):
        random_x = np.random.uniform(0, box_width)
        random_y = np.random.uniform(0, box_height)
        ptcle = Particle(random_x, random_y)
        particle_array.append(ptcle)

    # Box with initial starting configuration
    box = Box(box_width, box_height, particle_array)

    points, = ax.plot(box.get_x_array(), 'o', c='red', markersize=5)
    ax.set_ylim(0, box_height)
    ax.set_xlim(0, box_width)

    ani = animation.FuncAnimation(fig, metropolis, frames=np.arange(0, num_steps), fargs=(box, temp, num_particles, points),
                                  interval=1)

    plt.grid()
    plt.title("Metropolis-Hastings Gas Simulation. %d particles at %d K" % (num_particles, temp))
    plt.show()

run(300, 1, 1, 10000, 4000)
