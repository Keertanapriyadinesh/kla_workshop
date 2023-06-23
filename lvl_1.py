# # -*- coding: utf-8 -*-
# """
# Created on Fri Jun 23 10:20:04 2023

# @author: HP
# """

from PIL import Image
import numpy as np  
import csv      
import json
import cv2


def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def load_images(file_path):
    images = []
    for i in range(1, 6):
        filename = f'{file_path}/wafer_image_{i}.png'
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        images.append(image)
    return images

# def create_image(images):
#     widths, heights = zip(*(i.size for i in images))
#     total_width = sum(widths)
#     max_height = max(heights)
#     new_img = Image.new('RGB', (total_width, max_height))

#     x_offset = 0
#     for image in images:
#         new_img.paste(image, (x_offset, 0))
#         x_offset += image.size[0]

#     return new_img


def partition_dies(image, die_x, die_y):
    x1, y1 = 0, 0
    x2, y2 = die_x, die_y
    dies = []
    while x2 <= image.size[0]:
        while y2 <= image.size[1]:
            dies.append(image.crop((x1, y1, x2, y2)))
            y1 += die_y
            y2 += die_y
        x1 += die_x
        x2 += die_x
        y1, y2 = 0, die_y
    return dies



if __name__ == '__main__':
    images = load_images('C:/Users/HP/Desktop/psg/KLA/Level_1_Input_Data')
    data = load_data('C:/Users/HP/Desktop/psg/KLA/Level_1_Input_Data/input.json')
    print(data)
    die_x=data['die']['width']
    die_y=data['die']['height']
    print(die_x,die_y)
    x1= data['care_areas'][0]['top_left']['x']
    y1= data['care_areas'][0]['top_left']['y']
    x2= data['care_areas'][0]['bottom_right']['x']
    y2= data['care_areas'][0]['bottom_right']['y']
    print(x1,y1)
    print(x2,y2)
    exclusion_zone=tuple(data['exclusion_zones'])
    print(exclusion_zone)
    images = load_images('C:/Users/HP/Desktop/psg/KLA/Level_1_Input_Data')
    #new_img = create_image(images)
    #dies = partition_dies(new_img, die_x, die_y)
    #for i, die in enumerate(dies):
     #   die.save(f'die_{i+1}.png')    

    height, width = images[0].shape
    diffs = []
    for i in range(len(images)-1):
        if i == len(images)-1:
            diff = cv2.compare(images[i], images[0], cv2.CMP_NE)
            diffs.append(diff)
        else:
            diff = cv2.compare(images[i], images[i+1], cv2.CMP_NE)
            diffs.append(diff)

    with open('defect_coordinates.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for x in range(width):
            for y in range(height):
                for i, diff in enumerate(diffs):
                    if diff[y, x] == 255:
                        writer.writerow([i+2,x, height-1-y])



