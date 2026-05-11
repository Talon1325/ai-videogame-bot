# Author: Talon Vorpahl
# Hardcoded bot to shot at every target within a 3x3 grid on aimlabs
import pydirectinput
from time import sleep
import time

AIMLABS_3x3_GRID = 30

def main():

    # Starts after 5 seconds of hitting run
    print("Starting", end = " ")
    for i in range (0,5):
        sleep(1)
        print(".", end= " ")
    

    # This moves to the restart button
    pydirectinput.moveTo(x=965, y=773)
    pydirectinput.click()

    # This accepts warning to restart
    pydirectinput.moveTo(x=818, y=600)
    pydirectinput.click()

    
    # Center coordinates of my monitor
    center = (959, 539)
    # The direction of where to move the moose
    direction = [(0,0), (1,1), (-1,-1), (0,1), (1,0), (0,-1), (-1,0), (1,-1), (-1,1)]
    
    # After firing return back to original positionat at Point(x=959, y=539) to recenter coordinate location for each shot
    pydirectinput.moveTo(center[0],center[1])

    leave = True
    start = time.time()
    sleep(1)

    # Requires player to click to start the game
    pydirectinput.click()

    # Takes 5 seconds for game to start
    sleep(5)

    while leave:
        end = time.time()

        # The duration of Aimlabs 3x3 grid gamemode is 30 seconds
        if end - start > AIMLABS_3x3_GRID:
            leave = False
        
        # Move cursor in each direction
        for i in direction:
            fire(i[0], i[1])

    print("End")


# Moves mouse in all 8 directions from the center and recenter's mouse for next direction
# movex - 0, -1, 1, for each direction on the x coordinate
# movey - 0, -1, 1, for each direction on the y coordinate
def fire(movex, movey):
    pydirectinput.move(400*movex, 400*movey,relative=True)
    pydirectinput.click()
    pydirectinput.move(-400*movex, -400*movey,relative=True)
    pydirectinput.click()



if __name__ == "__main__":
    main()