from PIL import Image, ImageDraw, ImageFont
import time
import threading
import random
import matplotlib.pyplot as plt
import numpy as np

# Load the image
image_path = "philo.png"
image = Image.open(image_path)

# Define positions for each philosopher's status (manually determined)
positions = {
    'Plato': (670, 470),  # Adjust based on the image
    'Confucius': (460, 770),
    'Aristotle': (490, 130),
    'Descartes': (290, 800),
    'Kant': (70, 460)
}

# Status dictionary to hold current status for each philosopher
statuses = {
    'Aristotle': 'Thinking',
    'Confucius': 'Waiting',
    'Descartes': 'Eating',
    'Kant': 'Waiting',
    'Plato': 'Thinking'
}

# Function to simulate status changes
def simulate_philosopher_status():
    possible_states = ['Thinking', 'Waiting', 'Eating']
    while True:
        for name in statuses.keys():
            statuses[name] = random.choice(possible_states)
        time.sleep(2)

# Main function to update and display the image with statuses
def main():
    # Start the status simulation in a separate thread
    status_thread = threading.Thread(target=simulate_philosopher_status)
    status_thread.daemon = True
    status_thread.start()

    # Matplotlib setup
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()

    while True:
        # Create an updated image
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)

        # Set a larger font size and a custom font
        font_size = 24
        try:
            font = ImageFont.truetype("arial.ttf", font_size)  # Use a custom font
        except IOError:
            font = ImageFont.load_default()  # Fallback if custom font is unavailable

        # Draw text for each philosopher with larger and thicker text
        for name, position in positions.items():
            status = statuses[name]
            x, y = position
            text = f'{name}: {status}'

            # Draw a "thick" effect by layering the text
            for offset in [-1, 1]:
                draw.text((x + offset, y), text, fill="black", font=font)
                draw.text((x, y + offset), text, fill="black", font=font)
            draw.text(position, text, fill="black", font=font)  # Main white text

        # Convert the PIL image to a NumPy array and display it
        ax.clear()
        ax.imshow(np.array(annotated_image))
        ax.axis('off')
        plt.draw()
        plt.pause(2)  # Pause for 2 seconds to simulate dynamic updates

if __name__ == "__main__":
    main()
