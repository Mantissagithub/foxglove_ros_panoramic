import cv2
import numpy as np

# Function to capture images from the camera
def capture_images():
    images = []
    capture = cv2.VideoCapture(0)  # 0 corresponds to the default camera

    # Capture 3 images
    for _ in range(3):
        ret, frame = capture.read()
        if not ret:
            print("Failed to capture image")
            break
        images.append(frame)
        cv2.imshow("Captured Image", frame)
        cv2.waitKey(2000)  # Wait for 2 seconds between captures

    capture.release()
    cv2.destroyAllWindows()

    return images

# Function to stitch the captured images into a panorama
def stitch_images(images):
    # Create a Stitcher object
    stitcher = cv2.Stitcher_create()

    # Stitch the images
    status, panorama = stitcher.stitch(images)

    # Check if the stitching was successful
    if status == cv2.Stitcher_OK:
        # Resize the panorama to your desired dimensions
        desired_width = 1280   # Change this to your desired width
        desired_height = 720  # Change this to your desired height
        panorama = cv2.resize(panorama, (desired_width, desired_height))

        # Display the panorama
        cv2.imshow("Panorama", panorama)
        cv2.waitKey(0)

        # Save the panorama image
        cv2.imwrite("panorama.jpg", panorama)
        print("Panorama successfully created and saved as 'panorama.jpg'")
    else:
        print("Panorama Stitching failed !")

# Capture images from the camera
captured_images = capture_images()

# Stitch the captured images into a panorama
if captured_images:
    stitch_images(captured_images)