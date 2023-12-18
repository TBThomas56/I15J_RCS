import os
import cv2
from Canny_Edge import Canning, thresholding

# folder path
dir_path = "data/task_lights_on"
count = 0
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1

for i in range(count):
    image = cv2.imread(f"data/task_lights_on/{i+1}.jpg", 0)
    thresholding(image, 0)
    Canning(image)


# # Collect Images
# cv2.imshow("Lights on", rescaleFrame(image))
