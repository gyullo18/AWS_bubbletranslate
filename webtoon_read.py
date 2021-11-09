import json
from PIL import Image
import easyocr
import cv2
from matplotlib import pyplot as plt

# json 파일
with open('./json/00279.json', 'r') as f:
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
    x_min = bubble_list['points'][0][0]
    y_min = bubble_list['points'][0][1]
    x_max = bubble_list['points'][0][0]
    y_max = bubble_list['points'][0][1]

    for i in range(1, len(bubble_list['points'])):
        if x_min > bubble_list['points'][i][0]:
            x_min = bubble_list['points'][i][0]
        if x_max < bubble_list['points'][i][0]:
            x_max = bubble_list['points'][i][0]
        if y_min > bubble_list['points'][i][1]:
            y_min = bubble_list['points'][i][1]
        if y_max < bubble_list['points'][i][1]:
            y_max = bubble_list['points'][i][1]

    return x_min, y_min, x_max, y_max

x_min, y_min, x_max, y_max = points(bubble[0])
print(x_min, y_min, x_max, y_max)
# print(bubble[0])

image_path = "./images/00279.jpg"
# tmp = image_path.split('/')
img = Image.open(image_path)
area = (x_min, y_min, x_max, y_max)
crop_img = img.crop(area)


# crop_img.show()

# easy_ocr
size = (512, 512)
crop_img = crop_img.resize(size)
crop_path = "./crop_images/crop_" + image_path.split('/')[-1]
crop_img.save(crop_path)

crop_img = cv2.imread(crop_path)
gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(bfilter, 30, 200)
cv2.imshow('edged', edged)
cv2.waitKey(0)
cv2.imwrite(crop_path, edged)
reader = easyocr.Reader(['ko', 'en'], gpu=False)
result = reader.readtext(crop_path)
print(result)