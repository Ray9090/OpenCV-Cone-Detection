import sys
import cv2 as cv
import numpy as np
import datetime
import os


def main(argv):
    # Default input image
    default_file = 'image/image2.png'
    filename = argv[0] if len(argv) > 0 else default_file ## buji nai

    # Load the input image
    input_image = cv.imread(filename, cv.IMREAD_COLOR)
    if input_image is None:
        print(f"Error: Image not found at {filename}")
        return

    t1 = datetime.datetime.now()

    # Convert the image to HSV color space
    hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV)

    # Define HSV ranges for different cone colors
    cone_colors = {
        "Blue": ((77, 150, 50), (130, 255, 255)),  # Blue cones
        "Orange": ((4, 150, 100), (20, 255, 255)),  # Orange cones
        "Yellow": ((20, 100, 110), (40, 255, 255))  # Yellow cones
    }

    # Initialize a mask for co2mentation
    color_segmented = np.zeros(hsv.shape[:2], dtype=np.uint8)
    color_labels = {}

    for color_name, (lower, upper) in cone_colors.items():
        mask = cv.inRange(hsv, lower, upper)
        color_segmented = cv.bitwise_or(color_segmented, mask)
        color_labels[color_name] = mask

    # Load the cone template in grayscale
    template_path = "reference/cone_template.png"
    cone_template = cv.imread(template_path, cv.IMREAD_GRAYSCALE)
    if cone_template is None:
        print("Error: Cone template image not found.")
        return

    # Apply Region of Interest (ROI)
    roi = apply_region_of_interest(color_segmented, input_image)

    # Container for detected rectangles
    rects = []

    # Iterate over multiple scales for template matching
    for i in range(1, 20):
        # Resize the template to different scales
        scale_factor = 1 / 4 + (i / 10)
        tmp_resize = cv.resize(
            cone_template,
            (
                max(int(cone_template.shape[1] * scale_factor), 1),
                max(int(cone_template.shape[0] * scale_factor), 1),
            ),
        )

        # Perform template matching
        res = cv.matchTemplate(roi, tmp_resize, cv.TM_CCORR_NORMED)

        # Apply a threshold to the results
        threshold = 0.6
        loc = np.where(res >= threshold)

        # Append the detected rectangles
        for pt in zip(*loc[::-1]):
            rects.append((
                int(pt[0]),  # x
                int(pt[1]),  # y
                int(tmp_resize.shape[1]),  # width
                int(tmp_resize.shape[0]),  # height
                res[pt[1], pt[0]],  # match score
                scale_factor  # scale factor
            ))

    # Filter overlapping detections
    filtered_rects = apply_non_maximum_suppression(rects)

    # Draw rectangles and labels around detected cones
    for rect in filtered_rects:
        x, y, w, h = rect[:4]
        input_image = cv.rectangle(input_image, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

        # Determine color label for the detection
        color_label = get_cone_color(hsv, x, y, w, h, cone_colors)
        cv.putText(input_image, color_label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the results
    #cv.imshow("Detected Cones", input_image)
    #cv.imshow("Color Segmented", color_segmented)

    t2 = datetime.datetime.now()
    print(f"Processing time: {(t2 - t1).total_seconds()} seconds")
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Save the output image
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output_detected_cones.jpg")
    cv.imwrite(output_path, input_image)
    print(f"Output image saved to {output_path}")


def apply_region_of_interest(mask, image):
    """
    Apply a region of interest (ROI) to the mask to remove unwanted areas.
    """
    height, width = image.shape[:2]
    roi = np.zeros((height, width), dtype=np.uint8)

    # Focus on the road area
    cv.rectangle(roi, (0, int(height * 0.2)), (width, height), 255, -1)
    return cv.bitwise_and(mask, roi)


def apply_non_maximum_suppression(rects):
    """
    Apply non-maximum suppression (NMS) to remove overlapping rectangles.
    """
    if not rects:
        return []

    # Sort rectangles by match score (descending)
    rects = sorted(rects, key=lambda x: x[4], reverse=True)

    nms_rects = []
    while rects:
        # Take the rectangle with the highest score
        best = rects.pop(0)
        nms_rects.append(best)

        # Remove overlapping rectangles
        rects = [
            rect for rect in rects
            if not overlap(best, rect)
        ]

    return nms_rects


def overlap(rect1, rect2):
    """
    Check if two rectangles overlap.
    """
    x1, y1, w1, h1 = rect1[:4]
    x2, y2, w2, h2 = rect2[:4]

    # Calculate overlap
    overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))

    overlap_area = overlap_x * overlap_y
    rect1_area = w1 * h1
    rect2_area = w2 * h2

    # Check if overlap area is significant
    return overlap_area > 0.5 * min(rect1_area, rect2_area)


def get_cone_color(hsv, x, y, w, h, cone_colors):
    """
    Determine the color of the detected cone by checking the HSV mask.
    """
    cropped_hsv = hsv[y:y + h, x:x + w]
    max_overlap = 0
    detected_color = "Unknown"

    for color_name, (lower, upper) in cone_colors.items():
        mask = cv.inRange(cropped_hsv, lower, upper)
        overlap = cv.countNonZero(mask)
        if overlap > max_overlap:
            max_overlap = overlap
            detected_color = color_name

    return detected_color


if __name__ == "__main__":
    main(sys.argv[1:])
