import random, json, math
from turtle import speed

class Trolley:
    def __init__(self, id):
        self.id = id
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.battery = 100.0
        self.basket_kg = 0.0

    def step(self, dt=1.0):
        speed = random.uniform(0, 1.4) # m/s
        self.heading += random.uniform(-0.3, 0.3) # radians
        self.x += speed*dt*math.cos(self.heading)
        self.y += speed*dt*math.sin(self.heading)
        self.battery = max(0, self.battery - 0.05)
        return {"id":self.id,"x":round(self.x,2),"y":round(self.y,2),
            "battery":round(self.battery,1)}

fleet=[Trolley(i) for i in range(3)]
for _ in range(20):
    for t in fleet:
        print(json.dumps(t.step()))