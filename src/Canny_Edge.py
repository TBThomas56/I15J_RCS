import cv2
from matplotlib import pyplot as plt
import numpy as np


def rescaleFrame(frame, scale=0.60):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


def thresholding(image, plot):
    a: dict = {}
    for i in range(50, 121, 5):
        ret, a[str(i)] = cv2.threshold(image, i, 0, cv2.THRESH_TOZERO)

    # Thresholding - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html

    if plot == 1:
        # Plotting
        titles = list(a.keys())
        images = list(a.values())
        length = (len(titles) // 2) + 1
        for i in range(len(titles)):
            plt.subplot(2, length, i + 1), plt.imshow(
                images[i], "gray", vmin=0, vmax=255
            )
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        plt.show()

    return a


def Canning(image):
    a = thresholding(image, 0)

    a50_edges_canny = cv2.Canny(a["50"], 150, 250)
    a50_edges_gauss = cv2.GaussianBlur(a["50"], (5, 5), 0)

    detected_circles = cv2.HoughCircles(
        a50_edges_gauss,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=100,
        param1=225,
        param2=67,
        minRadius=160,
        maxRadius=300,
    )

    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(image, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(image, (a, b), 50, (0, 0, 255), 3)

    # show Canny Edge Detection
    a50_resized = rescaleFrame(a50_edges_canny)

    cv2.imshow("circles", rescaleFrame(image))
    cv2.imshow("edges", a50_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
