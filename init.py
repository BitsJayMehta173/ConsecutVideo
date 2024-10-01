import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Function to show frame with only the uncommon pixels updated
def show_frame(diff_frame, label):
    # Convert the frame from BGR (OpenCV format) to RGB (Tkinter format)
    frame_rgb = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to a PIL image
    image = Image.fromarray(frame_rgb)
    
    # Convert the PIL image to a format that Tkinter can display
    imgtk = ImageTk.PhotoImage(image=image)
    
    # Update the Tkinter label with the new image
    label.imgtk = imgtk  # Keep a reference to avoid garbage collection
    label.config(image=imgtk)

# Function to update the video frame
def update_frame():
    global frame_count, prev_frame

    # Read the next frame from the video
    ret, frame = cap.read()

    if ret:
        # If we have a previous frame to compare to
        if prev_frame is not None:
            # Compute absolute difference between current frame and previous frame
            diff = cv2.absdiff(frame, prev_frame)

            # Create a mask where the differences are greater than a threshold
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

            # Create a 3-channel mask to apply to the BGR image
            mask_3ch = cv2.merge([mask, mask, mask])

            # Update only the uncommon pixels from the current frame
            uncommon_pixels = cv2.bitwise_and(frame, mask_3ch)

            # Combine uncommon pixels with previous frame
            combined_frame = cv2.add(prev_frame, uncommon_pixels)
        else:
            combined_frame = frame

        # Display the frame with only the uncommon pixels updated
        show_frame(combined_frame, label)

        # Save the current frame as the previous frame for the next iteration
        prev_frame = frame

        # Increment the frame counter
        frame_count += 1
        
        # Call this function again after 30ms to simulate video playback
        root.after(30, update_frame)
    else:
        # End of video or error reading the frame
        cap.release()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Uncommon Pixels Video")

# Create a Label widget to display the frame
label = tk.Label(root)
label.pack()

# Open the video file
video_path = 'ra.wmv'
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    exit()

# Frame counter and previous frame initialization
frame_count = 0
prev_frame = None

# Start the frame update process
update_frame()

# Start the Tkinter main loop
root.mainloop()
