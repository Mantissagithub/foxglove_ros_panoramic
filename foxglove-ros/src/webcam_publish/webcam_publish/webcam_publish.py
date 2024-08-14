import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
import numpy as np

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('webcam_publisher')
        self.publisher_ = self.create_publisher(Image, '/image_raw', 10)
        # Change to the IP camera URL
        self.cap = cv2.VideoCapture('http://192.168.120.191:5000/video_feed')  # Update the endpoint if needed
        self.bridge = CvBridge()
        self.images = []  # List to store captured frames
        self.capture_count = 0  # Counter for captured images
        self.max_captures = 5  # Number of frames to capture for 120 degrees
        self.width = 1280  # Set desired width
        self.height = int(self.width / 3)  # Calculate height for 1:3 ratio

    def capture_frames(self):
        while self.capture_count < self.max_captures:
            ret, frame = self.cap.read()
            if ret:
                # Resize the frame to maintain a 1:3 aspect ratio
                frame_resized = cv2.resize(frame, (self.width, self.height))
                
                # Display the captured frame for verification (optional)
                cv2.imshow('Captured Frame', frame_resized)
                cv2.waitKey(1)  # Display the frame for a brief moment

                # Store the resized frame
                self.images.append(frame_resized)
                self.capture_count += 1
                self.get_logger().info(f"Captured image {self.capture_count}/{self.max_captures}")

                # Wait for 2 seconds before capturing the next frame
                time.sleep(2)

        self.stitch_and_publish()

    def stitch_and_publish(self):
        self.get_logger().info(f"Stitching {len(self.images)} images...")
        
        for img in self.images:
            self.get_logger().info(f"Image shape: {img.shape}, dtype: {img.dtype}")
        
        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)  # Use panorama mode
        error, stitched_img = stitcher.stitch(self.images)  # Stitch all captured frames

        if error == cv2.Stitcher_OK:
            self.get_logger().info("Stitching successful!")
            # Convert the stitched image to a ROS Image message
            msg = self.bridge.cv2_to_imgmsg(stitched_img, "bgr8")
            self.publisher_.publish(msg)
            self.get_logger().info("Stitched image published.")
            # Optionally save the stitched image locally
            cv2.imwrite('stitched_image.jpg', stitched_img)
            self.get_logger().info("Stitched image saved as 'stitched_image.jpg'.")
        else:
            self.get_logger().error("Images could not be stitched!")
            self.get_logger().error(f"Error code: {error}")

        # Reset for the next capture cycle
        self.images.clear()
        self.capture_count = 0

    def destroy_node(self):
        self.cap.release()  # Release the video capture object
        cv2.destroyAllWindows()  # Close all OpenCV windows
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    webcam_publisher = WebcamPublisher()
    webcam_publisher.capture_frames()  # Start capturing frames
    webcam_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()