# Joseph Michael Coffey IV – jmichaelc4@gmail.com – jmcoffey@colostate.edu 
# Hayden Corbin - haydenfcorbin@gmail.com - hayden.corbin@colostate.edu 
# Reilly Bergeron - reillybergeron@gmail.com - reillyjb@colostate.edu 

"""
Source 1 - https://stackoverflow.com/questions/48364168/flickering-video-in-opencv-tkinter-integration
Source 2 - https://towardsdatascience.com/finding-most-common-colors-in-python-47ea0767a06a
"""

from EventHandler import EventHandler
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
import cv2


running_video = True


def get_video_frames(capture_obj, width, height):
    width_by_height = (width, height)
    ret, frame = capture_obj.read()
    if not ret:
        print("Failed to read stream? exiting")
        exit(1)

    frame = cv2.resize(frame, width_by_height)

    color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame, color_frame


def add_frame_to_label(video_label, color_frame):
    global running_video
    try:
        img = Image.fromarray(color_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.config(image=imgtk)
        video_label.image = imgtk  # Source 1 - This one line stops flickering
        
        return True
    
    except RuntimeError:
        running_video = False
        
        return False


def get_common_colors(arg_list):
    color_frame, rgb_queue, frame_queue = arg_list    
    most_common_colors = KMeans(n_clusters=6, n_init="auto")  # Used and adapted from a website
    most_common_colors.fit(color_frame.reshape(-1, 3))  # Used and adapted from a website
    if len(rgb_queue) <= 0:
        rgb_queue.appendleft(most_common_colors.cluster_centers_)
        
    while len(frame_queue) > 0:
        frame_queue.pop()


def run_video(frame_queue, rgb_queue, event_queue, screen_width, screen_height):
    global running_video

    handler = EventHandler()
    handler.add_event("get_common_colors", get_common_colors)

    width = int(screen_width / 2)
    height = int(screen_height / 2) + int(screen_height / 8)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to get from camera, exiting")
        exit(1)

    while running_video:
        frame, color_frame = get_video_frames(cap, width, height)
        frame_queue.appendleft(color_frame)

        while len(event_queue) > 0:
            handler.handle_event((event_queue.pop(), [color_frame, rgb_queue, frame_queue]))

    cap.release()
    cv2.destoryAllWindows()
