import json
from PIL import Image
import easyocr
import cv2
from matplotlib import pyplot as plt
import math # math.dist 두 점 사이의 거리

# json 파일
with open('./json/00284.json', 'r') as f:
    json_data = json.load(f)
    json_shape = json_data['shapes']
# print(json.dumps(json_data))
# print(len(json_shape))

bubble = []
for i in range(len(json_shape)):
    if "bubble" in json_shape[i]['label']:
        # print(json_shape[i])
        bubble.append(json_shape[i])

print(type(json_shape[i]))
print(type(bubble))

# print(bubble)
def points(bubble_list: list):
    bubble_result = []
    for i in range(len(bubble_list)):
        x_min = bubble_list[i]['points'][0][0]
        y_min = bubble_list[i]['points'][0][1]
        x_max = bubble_list[i]['points'][0][0]
        y_max = bubble_list[i]['points'][0][1]

        for j in range(1, len(bubble_list[i]['points'])):
            if x_min > bubble_list[i]['points'][j][0]:
                x_min = bubble_list[i]['points'][j][0]
            if x_max < bubble_list[i]['points'][j][0]:
                x_max = bubble_list[i]['points'][j][0]
            if y_min > bubble_list[i]['points'][j][1]:
                y_min = bubble_list[i]['points'][j][1]
            if y_max < bubble_list[i]['points'][j][1]:
                y_max = bubble_list[i]['points'][j][1]

        bubble_result.append([x_min, y_min, x_max, y_max])


    return bubble_result


r_bubble = points(bubble)

for i in range(len(r_bubble)):
    image_path = "./images/00284.jpg"
    img = Image.open(image_path)
    area = tuple(r_bubble[i])
    crop_img = img.crop(area)
    # size = (512, 512)
    # crop_img = crop_img.resize(size)
    crop_path = "./crop_images/crop_" + str(i) +"_" + image_path.split('/')[-1]
    crop_img.save(crop_path)

# x_min, y_min, x_max, y_max = points(bubble[0])
# print(x_min, y_min, x_max, y_max)
# # print(bubble[0])

# image_path = "./images/00279.jpg"
# # tmp = image_path.split('/')
# img = Image.open(image_path)
# area = (x_min, y_min, x_max, y_max)
# crop_img = img.crop(area)
#
#
# # crop_img.show()
#
# # easy_ocr
# size = (512, 512)
# crop_img = crop_img.resize(size)
# crop_path = "./crop_images/crop_" + image_path.split('/')[-1]
# crop_img.save(crop_path)
