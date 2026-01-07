import cv2
import numpy as np

# -------------------------------
# Create circular lane icons A/B/C/D
# -------------------------------

def make_lane(label, filename):
    img = np.ones((200,200,3),dtype=np.uint8)*255  # white background

    # Draw outer border circle (black)
    cv2.circle(img, (100,100), 90, (0,0,0), 8)

    # Fill circle (white)
    cv2.circle(img, (100,100), 86, (255,255,255), -1)

    # Put lane letter
    cv2.putText(img, label, (65,135),
                cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0,0,0), 8)

    cv2.imwrite(filename, img)


# Generate lane icons
make_lane("A", "laneA.png")
make_lane("B", "laneB.png")
make_lane("C", "laneC.png")
make_lane("D", "laneD.png")

print("Lane icons created ✔️")


# -------------------------------
# Create realistic round traffic lights
# -------------------------------

def make_light(color, filename):
    img = np.ones((200,200,3),dtype=np.uint8)*50  # grey traffic box bg
    cv2.circle(img, (100,100), 80, (0,0,0), 8)    # black border

    if color == "red":
        fill = (0,0,255)
    elif color == "yellow":
        fill = (0,255,255)
    elif color == "green":
        fill = (0,255,0)

    cv2.circle(img, (100,100), 70, fill, -1)     # fill circle

    cv2.imwrite(filename, img)

# Generate traffic light icons
make_light("red", "red.png")
make_light("yellow", "yellow.png")
make_light("green", "green.png")

print("Traffic lights created ✔️")
print("\nAll icons are ready to use!")
