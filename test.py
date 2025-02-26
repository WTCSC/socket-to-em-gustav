import time
import sys

def loading_effect():
    for _ in range(3):
        for dots in range(1, 4):
            sys.stdout.write('\r' + '.' * dots)  # '\r' moves the cursor to the start of the line
            sys.stdout.flush()  # Ensures the output is updated immediately
            time.sleep(0.5)  # Adds a delay between each dot update
    sys.stdout.write('\rDone!       \n')  # Final message after loading


print("a")
loading_effect()