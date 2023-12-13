# skimage coin with varying background

# # https://pyimagesearch.com/2016/02/08/opencv-shape-detection/
# contours, hierarchy = cv2.findContours(a["50"], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# for contour in contours:
#     approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
#     cv2.drawContours(a["50"], [approx], 0, (0, 0, 0), 5)
#     x = approx.ravel()[0]
#     y = approx.ravel()[1] - 5


# if len(approx) == 3:
#     cv2.putText(a["50"], "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
# elif len(approx) == 4:
#     x, y, w, h = cv2.boundingRect(approx)
#     aspectRatio = float(w) / h
#     print(aspectRatio)
#     if aspectRatio >= 0.95 and aspectRatio < 1.05:
#         cv2.putText(a["50"], "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

#     else:
#         cv2.putText(
#             a["50"], "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0)
#         )
