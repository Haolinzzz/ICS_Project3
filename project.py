from planets import planet, Probe
from math import sqrt

# Constants
G           = 6.67e-11          # Gravitational Constant
AU          = 1.5e11            # Astro Unit
DinS        = 24.0*60*60        # Day in Seconds

# initialization
start = "2024-04-26" # can modify the time by user

# define planets
sun = planet("Sun", 10, 2.0e30, start=start)
venus = planet("Venus", 299, 4.8673e24, start=start)
earth = planet("Earth", 399, 5.9722e24, start=start)
mars = planet("Mars", 499, 6.39e23 , start=start)

# this is the the space probe inital velocity's ratio to Earth
percentage = 1.15

# define the space probe object
probe = Probe(30, sun, venus, earth, mars, DinS, percentage)


# plotting
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
matplotlib.rcParams['animation.embed_limit'] = 2**128
from IPython.display import HTML

fig, subp = plt.subplots(figsize=(10,10))
subp.set_aspect('equal')
subp.grid()

#initial position
ip_venus = [0.72 * AU, 0]
ip_earth = [AU, 0]
ip_mars = [1.5 * AU, 0]
ip_probe = [1.5 * AU, 0]
ip_sun = [0, 0]

# Venus
orbit_v, = subp.plot([], [], '-', color='grey', lw=1)
planet_v, = subp.plot(*ip_venus, marker="o", markersize=4, markeredgecolor="grey", markerfacecolor="grey")
label_v = subp.text(*ip_venus, 'Venus')

# Earth
orbit_e, = subp.plot([], [], '-b', lw=1)
planet_e, = subp.plot(*ip_earth, marker="o", markersize=4, markeredgecolor="blue", markerfacecolor="blue")
label_e = subp.text(1.666 * AU, 0, 'Earth')

# Mars
orbit_m, = subp.plot([], [], '-r', lw=1)
planet_m, = subp.plot(*ip_mars, marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
label_m = subp.text(*ip_mars, 'Mars')

# Space Probe
orbit_p, = subp.plot([], [], '-', color='black', lw=1)
spaceprobe_p, = subp.plot(*ip_probe, marker="o", markersize=2, markeredgecolor="black", markerfacecolor="black")
label_p = subp.text(*ip_probe, 'Space Probe')

# Sun
planet_s, = subp.plot(*ip_sun, marker="o", markersize=8, markeredgecolor="yellow", markerfacecolor="yellow")
label_s = subp.text(*ip_sun, "Sun")

# Date label 
label_date = subp.text(-2.5 * 1E11, 2.4 * 1E11, earth.start)

# position track for each unit
venus_x, venus_y = [], []
earth_x, earth_y = [], []
mars_x, mars_y = [], []
probe_x, probe_y = [], []


def runOrbit(i):
    venus_x.append(venus.x[i])
    earth_x.append(earth.x[i])
    mars_x.append(mars.x[i])
    probe_x.append(probe.arr_x[i])
    
    venus_y.append(venus.y[i])
    earth_y.append(earth.y[i])
    mars_y.append(mars.y[i])
    probe_y.append(probe.arr_y[i])
    
    orbit_v.set_data(venus_x,venus_y)
    orbit_e.set_data(earth_x,earth_y)
    orbit_m.set_data(mars_x,mars_y)
    orbit_p.set_data(probe_x,probe_y)

    planet_v.set_data(venus.x[i],venus.y[i])
    planet_e.set_data(earth.x[i],earth.y[i])
    planet_m.set_data(mars.x[i],mars.y[i])
    spaceprobe_p.set_data(probe.arr_x[i],probe.arr_y[i])


    label_v.set_position((venus.x[i],venus.y[i]))
    label_e.set_position((earth.x[i],earth.y[i]))    
    label_m.set_position((mars.x[i],mars.y[i]))
    label_p.set_position((probe.arr_x[i],probe.arr_y[i]))

    subp.axis('equal')
    subp.set_xlim(-2.5*AU,2.5*AU)
    subp.set_ylim(-2.5*AU,2.5*AU)

    label_date.set_text(earth.d[i])

    return orbit_v,planet_v,label_v,orbit_e,planet_e,label_e,orbit_m,planet_m,label_m,orbit_p,spaceprobe_p,label_p,label_date

anim = animation.FuncAnimation(fig,func=runOrbit,frames=len(earth.x),interval=10,blit=True)
plt.show()
