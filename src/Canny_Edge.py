import cv2
from matplotlib import pyplot as plt
import numpy as np


def rescaleFrame(frame, scale=0.60):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


def dewarp(image, inputs, plot=0):
    # TODO: fix warping based off of image selection
    assert image is not None, "file could not be read, check with os.path.exists()"
    rows, cols = image.shape
    input_points = np.float32([inputs[0], inputs[1], inputs[2], inputs[3]])
    output_points = np.float32([[0, 0], [0, rows], [cols, rows], [cols, 0]])
    M = cv2.getPerspectiveTransform(input_points, output_points)
    dst = cv2.warpPerspective(image, M, (cols, rows))

    if plot == 1:
        cv2.imshow("originial", image)
        cv2.imshow("dewarped", dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return dst


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


def adding_circles(circles, image):
    for pt in circles[0, :]:
        x, y, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the circle.
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)

        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(image, (x, y), 5, (0, 0, 255), 3)

    cv2.imshow("circles", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image


def Canning(image):
    x = thresholding(image, 0)

    a50_edges_canny = cv2.Canny(x["50"], 150, 250)
    a50_edges_gauss = cv2.GaussianBlur(x["50"], (5, 5), 0)

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

    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        # output = np.zeros(np.shape(detected_circles)[1])
        output = []

        for pt in detected_circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            # Mask Image with Circle
            mask = np.zeros_like(image)
            mask = cv2.circle(mask, (x, y), r, (255, 255, 255), -1)

            masked = cv2.bitwise_and(image, image, mask=mask)

            # Check 2: Find small circles
            mini_circles = cv2.HoughCircles(
                masked,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=35,
                param1=225,
                param2=25,
                minRadius=1,
                maxRadius=25,
            )

            if mini_circles is not None:
                mini_circles = np.uint16(np.around(mini_circles))
                output.append("Puck")
                image_mini = adding_circles(mini_circles, masked)
            else:
                output.append("Lid")

        # TODO: Apply algorithm to try identify different pucks and lids. Create them in different data structures
        image_drawn = adding_circles(detected_circles, image)

    # show Canny Edge Detection

    # cv2.imshow("circles", image_drawn)
    cv2.imshow("edges", a50_edges_canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return output


# def detection(image,circle):
