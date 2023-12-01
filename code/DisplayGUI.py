# Joseph Michael Coffey IV – jmichaelc4@gmail.com – jmcoffey@colostate.edu 
# Hayden Corbin - haydenfcorbin@gmail.com - hayden.corbin@colostate.edu 
# Reilly Bergeron - reillybergeron@gmail.com - reillyjb@colostate.edu 

"""
Source 1 - https://www.tutorialspoint.com/how-to-get-the-screen-size-in-tkinter#:~:text=In%20order%20to%20get%20the,of%20the%20screen%20in%20pixels. 
Source 2 - https://www.tutorialspoint.com/how-can-i-prevent-a-window-from-being-resized-with-tkinter. 
Source 3 - https://www.plus2net.com/python/tkinter-rowconfigure.php. 
"""

import tkinter as tk
from RealtimeVideo import run_video, add_frame_to_label
from ColorEditor import change_color, set_artificial_bound
from ColorUIElement import ColorUIElement
import threading
from collections import deque

master_bgr_dict = {}
event_queue = deque()
max_deque_size = 1


def refresh_colors():
    global master_bgr_dict
    master_bgr_dict = {}

    event_queue.appendleft("get_common_colors")


def render_header(UI, screen_width, screen_height):
    header_frame = tk.Frame(master=UI, width=int(screen_width), height=int(screen_height/16), bg="red")
    
    temp_button = tk.Button(header_frame, height=1, width=18, bg="white", text="Refresh Frame", command=refresh_colors)
    temp_button.pack(fill=tk.BOTH, side=tk.RIGHT)

    scale = tk.Scale(master=header_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200,
                     command=lambda new_val: set_artificial_bound(new_val))
    scale.pack(fill=tk.BOTH, side=tk.LEFT)
    scale.set(30)

    return header_frame


def render_color_palette(UI, screen_width, screen_height):
    palette_frame = tk.Frame(master=UI, width=int(screen_width), height=int(screen_height/6), bg="yellow")
    return palette_frame


def print_color(color_val):
    print(color_val)


def set_global_rgb_vals(color_ui_element):
    global master_bgr_dict
    master_bgr_dict[color_ui_element.color_name] = (color_ui_element.org_bgr, color_ui_element.bgr)


def render_buttons(color_palette_frame, button_array, button_label_width, button_label_height):
    for button in button_array:
        new_element = ColorUIElement(color_palette_frame, button, button_label_width, button_label_height)
        new_element.set_button_command(lambda a: set_global_rgb_vals(a))


def main():
    running = True
    UI = tk.Tk()
    UI.resizable(width=False, height=False)     # Used from Tutorials Point
    
    screen_width = UI.winfo_screenwidth() - int((UI.winfo_screenwidth()) / 24)     # Adapted from Tutorials Point
    screen_height = UI.winfo_screenheight() - int((UI.winfo_screenheight()) / 8)     # Adapted from Tutorials Point
    UI.geometry("%dx%d" % (screen_width, screen_height))     # Used from Tutorials Point
    
    frame_queue = deque()
    rgb_queue = deque()
    changed_frames_queue = deque()

    custom_camera_title_frame = render_header(UI, screen_width, screen_height)

    before_color_change_frame = tk.Frame(master=UI, width=int(screen_width),
                                         height=int(screen_height / 2) + int(screen_height / 8), bg="blue")
    video_label = tk.Label(master=before_color_change_frame)
    video_label.pack(fill=tk.BOTH, side=tk.LEFT)
    second_video = tk.Label(master=before_color_change_frame)
    second_video.pack(fill=tk.BOTH, side=tk.RIGHT)

    color_palette_frame = render_color_palette(UI, screen_width, screen_width)
    
    UI.rowconfigure(0, weight=2)     # Adapted from plus2net
    UI.rowconfigure(1, weight=1)     # Adapted from plus2net
    UI.rowconfigure(2, weight=2)     # Adapted from plus2net
    
    UI.columnconfigure(0, weight=1)     # Adapted from plus2net
    UI.columnconfigure(1, weight=1)     # Adapted from plus2net
    
    custom_camera_title_frame.grid(row=0, column=0)

    before_color_change_frame.grid(row=1, column=0)
    
    color_palette_frame.grid(row=2, column=0)

    event_queue.appendleft("get_common_colors")
    video_input_thread = threading.Thread(target=run_video, args=(frame_queue, rgb_queue, event_queue, screen_width,
                                                                  screen_height))
    video_input_thread.start()

    # Input colors as BGR
    while running:
        global master_bgr_dict, max_deque_size

        try:
            color_frame = frame_queue.pop()
            
            color_change_thread = threading.Thread(target=change_color, args=(color_frame, master_bgr_dict,
                                                                              changed_frames_queue))
            color_change_thread.start()

            running = add_frame_to_label(video_label, color_frame)

            color_change_thread.join()
            changed_frame = changed_frames_queue.pop()
            add_frame_to_label(second_video, changed_frame)
            
            if len(frame_queue) > max_deque_size:
                frame_queue.clear()
                changed_frames_queue.clear()
            
        except IndexError:
            pass

        if len(rgb_queue) > 0:
            rgb_array = rgb_queue.pop()
            color_palette_frame.destroy()
            color_palette_frame = render_color_palette(UI, screen_width, screen_width)
            color_palette_frame.grid(row=2, column=0)

            if len(rgb_array) > 0 and rgb_array is not None:
                render_buttons(color_palette_frame, rgb_array, int(screen_width / 77), 2)

        # Goes after all updates
        UI.update()

    video_input_thread.join()


if __name__ == "__main__":
    main()
