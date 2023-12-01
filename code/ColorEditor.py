# Joseph Michael Coffey IV – jmichaelc4@gmail.com – jmcoffey@colostate.edu 
# Hayden Corbin - haydenfcorbin@gmail.com - hayden.corbin@colostate.edu 
# Reilly Bergeron - reillybergeron@gmail.com - reillyjb@colostate.edu 

"""
Source 1 - https://www.plus2net.com/python/tkinter-colors.php#google_vignette
Source 2 - https://stackoverflow.com/questions/1847092/given-an-rgb-value-what-would-be-the-best-way-to-find-the-closest-match-in-the-d
Source 3 - https://stackoverflow.com/questions/50210304/change-the-colors-within-certain-range-to-another-color-using-opencv
"""

import cv2
import numpy as np
import pandas as pd
import math


artificial_bound = 0


def set_artificial_bound(new_val):
    global artificial_bound
    artificial_bound = int(new_val)


def make_rgb_list(color_table):
    rgb_list = []

    red_list = color_table['Red'].values.tolist()
    green_list = color_table['Green'].values.tolist()
    blue_list = color_table['Blue'].values.tolist()

    for a in range(len(red_list)):
        rgb_list.append([red_list[a], green_list[a], blue_list[a]])

    return rgb_list


color_table = pd.read_excel('tables/tk-colours.xlsx')  # Source 1
color_dict = {}

names = color_table["Name"].values.tolist()
rgb_list = make_rgb_list(color_table)

for a in range(len(names)):
    color_dict[str(rgb_list[a])] = names[a]


def make_color_mask(color_frame, new_bgr):
    new_row = [new_bgr for pixel in range(len(color_frame[0]))]
    ret_mask = [new_row for row in range(len(color_frame))]

    return ret_mask


def calc_lower_upper(find_bgr):
    global artificial_bound
    lower = []
    upper = []

    for b in range(len(find_bgr)):  # Edit b, g, and r values
        sub_val = find_bgr[b] - artificial_bound if find_bgr[b] - artificial_bound > 0 else 0
        add_val = find_bgr[b] + artificial_bound if find_bgr[b] + artificial_bound < 255 else 255

        lower.append(sub_val)
        upper.append(add_val)

    return np.array(lower, dtype="uint8"), np.array(upper, dtype="uint8")


def change_color(color_frame, bgr_dict, changed_queue):
    for color in list(bgr_dict.keys()):
        lower, upper = calc_lower_upper(bgr_dict[color][0])

        mask = cv2.inRange(color_frame, lower, upper)
        color_frame[mask > 0] = bgr_dict[color][1][::-1]  # Source 3

    changed_queue.appendleft(color_frame)


def rgb_to_name(rgb_val):  # Source 2
    wr = 1  # 0.3
    wg = 1  # 0.59
    wb = 1  # 0.11
    try:
        color_name = color_dict[str(rgb_val)]
        return color_name

    except KeyError:
        min_diff = math.sqrt(math.pow(255 * wr, 2) +
                             math.pow(255 * wg, 2) +
                             math.pow(255 * wb, 2))
        found_ind = 0
        for d in range(len(rgb_list)):
            temp_diff = math.sqrt(math.pow((rgb_val[0] - rgb_list[d][0]) * wr, 2) +
                                  math.pow((rgb_val[1] - rgb_list[d][1]) * wg, 2) +
                                  math.pow((rgb_val[2] - rgb_list[d][2]) * wb, 2))
            if temp_diff < min_diff:
                min_diff = temp_diff
                found_ind = d

        color_name = color_dict[str(rgb_list[found_ind])]
        return color_name
