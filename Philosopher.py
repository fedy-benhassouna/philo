import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, name, left_chopstick, right_chopstick, color, neighbor):
        threading.Thread.__init__(self)
        self.stopped = False
        self.name = color + name + '\033[00m'
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.neighbor = neighbor  # Neighbor philosopher reference
        self.state = "thinking"  # State: thinking, hungry, eating

    def pickup(self):
        if not self.stopped:
            self.state = "hungry"
            print(f'{self.name} is hungry and consulting {self.neighbor.name}.')
            
            # Wait for neighbor to finish eating
            while self.neighbor.state == "eating":
                print(f'{self.name} is waiting for {self.neighbor.name} to finish eating.')
                time.sleep(1)

            # Acquire chopsticks
            self.left_chopstick.acquire()
            self.right_chopstick.acquire()
            self.state = "eating"

    def putdown(self):
        self.left_chopstick.release()
        self.right_chopstick.release()
        self.state = "thinking"

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            print(f'{self.name} is thinking.')
            time.sleep(random.randint(3, 15))  # Thinking

            print(f'{self.name} is waiting.')
            self.pickup()
            if self.stopped: return

            print(f'{self.name} is eating.')
            time.sleep(random.randint(3, 10))  # Eating
            self.putdown()

