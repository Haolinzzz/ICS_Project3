from planets import planet, Probe
from math import sqrt

#define the constant
G           = 6.67e-11
Ms          = 2.0e30             # Mass of sun
Mv          = 4.8673e24          # Mass of venus
Me          = 5.9722e24          # Mass of earth        
Mm          = 6.39e23            # Mass of mars
AU          = 1.5e11
DinS        = 24.0*60*60

# initialization
start = "2023-04-26" # can modify the time by user

sun = planet("Sun", 10, Ms, start=start)
venus = planet("Venus", 299, Mv, start=start)
earth = planet("Earth", 399, Me, start=start)
mars = planet("Mars", 499, Mm, start=start)

earth.z = [0 for i in range(len(earth.z))]
earth.vz = [0 for i in range(len(earth.vz))]

venus.z = [0 for i in range(len(venus.z))]
venus.vz = [0 for i in range(len(venus.vz))]

cur_v = sqrt((earth.vx[0]/DinS)**2 + (earth.vy[0]/DinS)**2 + (earth.vz[0]/DinS)**2)

# desired_v = cur_v + 4511
# perc_v = desired_v/cur_v

# print(cur_v)
# print(desired_v)
# print(perc_v)

percentage = 1.15

probe = Probe(30, sun, venus, earth, mars, DinS, percentage)


# plotting
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
matplotlib.rcParams['animation.embed_limit'] = 2**128
from IPython.display import HTML

fig, ax = plt.subplots(figsize=(10,10))
ax.set_aspect('equal')
ax.grid()

# initial_position_venus = [AU, 0]
# initial_position_earth = [1.5 * AU, 0]
# initial_position_mars = [2 * AU, 0]
# initial_position_probe = [2 * AU, 0]
# position_sun = [0, 0]

initial_position_venus = [0.72 * AU, 0]
initial_position_earth = [AU, 0]
initial_position_mars = [1.5 * AU, 0]
initial_position_probe = [1.5 * AU, 0]
position_sun = [0, 0]

# Venus
line_a, = ax.plot([], [], '-g', lw=1)
point_a, = ax.plot(*initial_position_venus, marker="o", markersize=4, markeredgecolor="brown", markerfacecolor="brown")
text_a = ax.text(*initial_position_venus, 'Venus')

# Earth
line_b, = ax.plot([], [], '-g', lw=1)
point_b, = ax.plot(*initial_position_earth, marker="o", markersize=3, markeredgecolor="blue", markerfacecolor="blue")
text_b = ax.text(1.666 * AU, 0, 'Earth')

# Mars
line_c, = ax.plot([], [], '-g', lw=1)
point_c, = ax.plot(*initial_position_mars, marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red")
text_c = ax.text(*initial_position_mars, 'Mars')

# Space Probe
line_d, = ax.plot([], [], '-g', lw=1)
point_d, = ax.plot(*initial_position_probe, marker="o", markersize=2, markeredgecolor="black", markerfacecolor="black")
text_d = ax.text(*initial_position_probe, 'Space Probe')

# Sun
point_e, = ax.plot(*position_sun, marker="o", markersize=8, markeredgecolor="yellow", markerfacecolor="yellow")
text_e = ax.text(*position_sun, "Sun")

# Date label 
text_date = ax.text(-2.5 * 1E11, 2.4 * 1E11, earth.start)

# position track for each unit
axdata, aydata = [], []
bxdata, bydata = [], []
cxdata, cydata = [], []
dxdata, dydata = [], []

# line_a,     = ax.plot([],[],'-g',lw=1)
# point_a,    = ax.plot([AU], [0], marker="o", markersize=4, markeredgecolor="brown", markerfacecolor="brown")
# text_a      = ax.text(AU,0,'Venus')

# line_b,     = ax.plot([],[],'-g',lw=1)
# point_b,    = ax.plot([1.5*AU], [0], marker="o", markersize=3, markeredgecolor="blue", markerfacecolor="blue")
# text_b      = ax.text(1.666*AU,0,'Earth')

# line_c,     = ax.plot([],[],'-g',lw=1)
# point_c,    = ax.plot([2*AU], [0], marker="o", markersize=2, markeredgecolor="red", markerfacecolor="red")
# text_c      = ax.text(2*AU,0,'Mars')

# line_d,     = ax.plot([],[],'-g',lw=1)
# point_d,    = ax.plot([2*AU], [0], marker="o", markersize=2, markeredgecolor="black", markerfacecolor="black")
# text_d      = ax.text(2*AU,0,'Space Probe')

# point_e     = ax.plot([0], [0], marker="o", markersize=8, markeredgecolor="yellow", markerfacecolor="yellow")
# text_e      = ax.text(0,0,"Sun")

# text_date   = ax.text(-2.5*1E11, 2.4*1E11, earth.start)

# axdata,aydata = [],[] # venus track
# bxdata,bydata = [],[] # earth track
# cxdata,cydata = [],[] # mars track
# dxdata,dydata = [],[] # space probe track

def runOrbit(i):
    axdata.append(venus.x[i])
    bxdata.append(earth.x[i])
    cxdata.append(mars.x[i])
    dxdata.append(probe.arr_x[i])
    
    aydata.append(venus.y[i])
    bydata.append(earth.y[i])
    cydata.append(mars.y[i])
    dydata.append(probe.arr_y[i])
    
    line_a.set_data(axdata,aydata)
    line_b.set_data(bxdata,bydata)
    line_c.set_data(cxdata,cydata)
    line_d.set_data(dxdata,dydata)

    point_a.set_data(venus.x[i],venus.y[i])
    point_b.set_data(earth.x[i],earth.y[i])
    point_c.set_data(mars.x[i],mars.y[i])
    point_d.set_data(probe.arr_x[i],probe.arr_y[i])


    text_a.set_position((venus.x[i],venus.y[i]))
    text_b.set_position((earth.x[i],earth.y[i]))    
    text_c.set_position((mars.x[i],mars.y[i]))
    text_d.set_position((probe.arr_x[i],probe.arr_y[i]))

    ax.axis('equal')
    ax.set_xlim(-2*AU,2*AU)
    ax.set_ylim(-2*AU,2*AU)

    text_date.set_text(earth.d[i])

    return line_a,point_a,text_a,line_b,point_b,text_b,line_c,point_c,text_c,line_d,point_d,text_d,text_date

anim = animation.FuncAnimation(fig,func=runOrbit,frames=len(earth.x),interval=10,blit=True)
plt.show()
