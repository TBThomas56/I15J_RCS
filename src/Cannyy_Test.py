import os
import cv2
from Canny_Edge import Canning, dewarp, rescaleFrame


def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Pointer at: {x},{y}")
        a.append([x, y])


# TODO: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
def calibration():
    image = cv2.imread(f"{dir_path}/1.jpg", 0)
    image = rescaleFrame(image)
    cv2.namedWindow("Point Coordinates")
    y = cv2.setMouseCallback("Point Coordinates", click_event)
    a.append(y)
    while True:
        cv2.imshow("Point Coordinates", image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
    cv2.destroyAllWindows()


# folder path
dir_path = "data/task_lights_on"
count = 0
a = []
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1

# TODO: Remove this once debugging of dewarping complete
# calibration()
# input_coordinates = [i for i in a if i is not None]

input_coordinates = [[120, 24], [150, 1202], [1332, 1211], [1330, 0]]

for i in range(count):
    image = cv2.imread(f"{dir_path}/{i+1}.jpg", 0)
    image = rescaleFrame(image)
    dewarped = dewarp(image, input_coordinates, 1)
    output = Canning(dewarped)
    print(output)
