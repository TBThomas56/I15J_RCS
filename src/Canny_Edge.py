import cv2
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget


def rescaleFrame(frame, scale=0.60):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


img_on = cv2.imread("data/task_lights_on/20.jpg", 0)
img_off = cv2.imread("data/task_lights_off/20.jpg", 0)

# Collect Images
cv2.imshow("Lights on", rescaleFrame(img_on))
cv2.imshow("Lights off", rescaleFrame(img_off))
cv2.waitKey(0)
cv2.destroyAllWindows()

a: dict = {}
for i in range(50, 121, 5):
    ret, a[str(i)] = cv2.threshold(img_on, i, 0, cv2.THRESH_TOZERO)

# Thresholding - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html

# Plotting
titles = list(a.keys())
images = list(a.values())
length = (len(titles) // 2) + 1
for i in range(len(titles)):
    plt.subplot(2, length, i + 1), plt.imshow(images[i], "gray", vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
# plt.show()


a50_edges = cv2.Canny(a["50"], 100, 200)


a50_resized = rescaleFrame(a50_edges)

cv2.imshow("edges", a50_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

app = QApplication([])
window = QWidget()
window.setWindowTitle("Thresholding and Canning Edge Detection")
window.show()
