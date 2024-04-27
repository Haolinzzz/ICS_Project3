from __future__ import annotations
from astroquery.jplhorizons import Horizons
from math import sqrt

G           = 6.67e-11
Ms          = 2.0e30             # sun
Mv          = 4.8673e24          # venus
Me          = 5.9722e24          # earth        
Mm          = 6.39e23            # mars
AU          = 1.5e11
DinS        = 24.0*60*60


class planet:
    autom: int = 149597870700
    step: str = "1d"
    start: str
    stop: str

    def __str__(self):
        return f"{self.name} with ID {self.id}"

    def setVector(self):
        obj = Horizons( id=self.id, location=None, epochs={'start':self.start, 'stop':self.stop, 'step':self.step})
        table = obj.vectors()
        
        self.x   = [ a * self.autom for a in table['x'] ]
        self.y   = [ b * self.autom for b in table['y'] ]
        self.z   = [ c * self.autom for c in table['z'] ]
        self.vx  = [ d * self.autom for d in table["vx"]]
        self.vy  = [ e * self.autom for e in table["vy"]]
        self.vz  = [ f * self.autom for f in table["vz"]]
        self.d   = [ g.split(" ")[1] for g in table["datetime_str"]] # for tracking the date

    def __init__(self, name, num, mass, start="2020-01-01", stop="2030-01-01"):
        self.name = name
        self.id = num
        self.mass = mass
        self.start = start
        self.stop = stop
        self.setVector()

class Probe:
    xv, yv, zv = 0,0,0
    arr_x,arr_y,arr_z = [],[],[]
    ptr = 0
    dt = DinS

    def CalculateGForce(self, planets, position, ptr):
        px, py, pz = position
        dx, dy, dz = 0,0,0

        for planet in planets:
            gravconst = G * planet.mass * self.mass
            
            # compute gravitation force on x, y, z
            rx,ry,rz = px - planet.x[ptr], py - planet.y[ptr], pz - planet.z[ptr]
            fx = -gravconst*rx/(rx**2+ry**2+rz**2)**1.5
            fy = -gravconst*ry/(rx**2+ry**2+rz**2)**1.5
            fz = -gravconst*rz/(rx**2+ry**2+rz**2)**1.5
        
            dx += fx
            dy += fy
            dz += fz         

        # compute acceleration and velocity 
        self.xv += dx*self.dt/self.mass
        self.yv += dy*self.dt/self.mass
        self.zv += dz*self.dt/self.mass
        
        # update current position
        px += self.xv*self.dt
        py += self.yv*self.dt 
        pz += self.zv*self.dt

        return px,py,pz
    
    # Validation for energy conservation
    def total_mechanical_energy(self, planets, ptr):
        # kinetic energy
        speed = sqrt(self.xv**2 + self.yv**2 + self.zv**2)
        kinetic_energy = 0.5 * self.mass * speed**2
        
        # potential energy
        potential_energy = 0
        for planet in planets:
            distance = sqrt((self.x - planet.x[ptr])**2 + (self.y - planet.y[ptr])**2 + (self.z - planet.z[ptr])**2)
            if distance != 0:
                potential_energy += -G * self.mass * planet.mass / distance

        # Total mechanical energy
        total_energy = kinetic_energy + potential_energy
        return total_energy
    
    def __init__(self, mass, sun, venus, earth, mars, timestep, v=1):
        self.earth = earth
        self.x = self.earth.x[0]
        self.y = self.earth.y[0]
        self.z = self.earth.z[0]
        self.xv = self.earth.vx[0]/timestep * v
        self.yv = self.earth.vy[0]/timestep * v
        self.zv = self.earth.vz[0]/timestep * v

        self.mass = mass
        self.dt = timestep 

        for i in range(len(earth.x)):
            x, y, z = self.CalculateGForce([sun, venus, mars], [self.x, self.y, self.z], self.ptr)
            self.ptr += 1

            self.x, self.y, self.z = x, y, z
            self.arr_x.append(x)
            self.arr_y.append(y)
            self.arr_z.append(z)
            
            ### this is the energy conservation validation part, since the animation will loops until manually stop,
            ### program will not automatically show the total mechanical energy.

            # total_energy = self.total_mechanical_energy([sun, venus, mars], self.ptr)
            # print(f"Total Mechanical Energy at step {self.ptr}: {total_energy}")