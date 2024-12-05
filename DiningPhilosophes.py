import sys
import random
import signal
from Philosopher import Philosopher
from chopstick import chopstick

# Define colors for philosophers
COLORS = {
    'red': '\033[0;31m',    # Red
    'yellow': '\033[33m',   # Yellow
    'green': '\033[32m',    # Green
    'blue': '\033[34m',     # Blue
    'purple': '\033[35m'    # Purple
} 

# Initialize chopsticks
chopsticks = [chopstick(f'c{i + 1}') for i in range(5)]
# Shuffle philosopher names for random seating
names = ['Aristotle', 'Confucius', 'Descartes', 'Kant', 'Plato']
random.shuffle(names)

# Create philosophers, assigning them adjacent chopsticks and neighbors
philosophers = []
for i in range(5):
    left_chopstick = chopsticks[i]
    right_chopstick = chopsticks[(i + 1) % 5]
    neighbor = philosophers[i - 1] if i > 0 else None
    philosopher = Philosopher(names[i], left_chopstick, right_chopstick, COLORS[list(COLORS.keys())[i]], neighbor)
    philosophers.append(philosopher)

# Ensure the last philosopher's neighbor is the first philosopher
philosophers[0].neighbor = philosophers[-1]

def initialize_dinner():
    """Print initial setup of the dinner."""
    print('Philosophers:')
    for philosopher in philosophers:
        print(f'{philosopher.name} ', end='')
    print('\n\nDinner is served!\n')

def start_dinner():
    """Start all philosopher threads."""
    for philosopher in philosophers:
        philosopher.start()
    for philosopher in philosophers:
        philosopher.join()

def end_dinner(signum, frame):
    """Handle graceful shutdown on interruption."""
    for philosopher in philosophers:
        philosopher.stop()
    print('\nDinner has ended. Waiting for everyone to finish up!\n')

if __name__ == '__main__':
    # Register signal handler for cleanup
    signal.signal(signal.SIGINT, end_dinner)

    # Initialize and start the simulation
    initialize_dinner()
    start_dinner()
    print("\nDone! 👌")
