import random, json, math

class Trolley:
    def __init__(self, trolley_id):
        self.id = trolley_id
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.battery = 100.0
        self.basket_kg = 0.0

    def step(self, dt=1.0):
        speed = random.uniform(0, 1.4)

        self.heading += random.uniform(-0.3, 0.3)

        self.x += speed * dt * math.cos(self.heading)
        self.y += speed * dt * math.sin(self.heading)

        self.battery = max(0, self.battery - 0.05)

        # Simulate products being added or removed
        basket_change = random.uniform(-0.2, 0.5)
        self.basket_kg = max(
            0,
            self.basket_kg + basket_change
        )

        return {
            "id": self.id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "speed": round(speed, 2),
            "heading": round(self.heading, 2),
            "battery": round(self.battery, 1),
            "basket_kg": round(self.basket_kg, 2)
        }

    def navigate_to(
        self,
        target_x,
        target_y,
        speed=1.0,
        dt=1.0
    ):
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.hypot(dx, dy)

        # Treat very small distances as arrival
        if distance <= 0.001:
            self.x = target_x
            self.y = target_y

            return {
                "id": self.id,
                "x": round(self.x, 2),
                "y": round(self.y, 2),
                "distance_remaining": 0.0,
                "status": "arrived"
            }

        self.heading = math.atan2(dy, dx)

        movement = min(speed * dt, distance)

        self.x += movement * math.cos(self.heading)
        self.y += movement * math.sin(self.heading)

        self.battery = max(
            0,
            self.battery - 0.05
        )

        distance_remaining = math.hypot(
            target_x - self.x,
            target_y - self.y
        )

        # Correct the final position
        if distance_remaining <= 0.001:
            self.x = target_x
            self.y = target_y
            distance_remaining = 0.0

        return {
            "id": self.id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "speed": round(speed, 2),
            "heading_radians": round(
                self.heading,
                3
            ),
            "heading_degrees": round(
                math.degrees(self.heading),
                1
            ),
            "distance_remaining": round(
                distance_remaining,
                2
            ),
            "battery": round(
                self.battery,
                1
            ),
            "status": (
                "arrived"
                if distance_remaining == 0
                else "moving"
            )
        }


# Test navigation to (6, 8)

trolley = Trolley(1)

target_x = 6
target_y = 8

while True:
    result = trolley.navigate_to(
        target_x,
        target_y,
        speed=1.0
    )

    print(json.dumps(result))

    if result["status"] == "arrived":
        break

print(
    "Final position:",
    trolley.x,
    trolley.y
)


# Test random fleet telemetry

fleet = [
    Trolley(i)
    for i in range(3)
]

# For testing navigation:

# for _ in range(20):
#    for trolley in fleet:
#        print(
#            json.dumps(
#                trolley.step()
#            )
#        )


# Required navigation maths

dx = 6
dy = 8

distance = math.hypot(dx, dy)
heading = math.atan2(dy, dx)

print(
    round(distance, 2),
    "distance units"
)

print(
    round(
        math.degrees(heading),
        1
    ),
    "degrees"
)