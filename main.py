import textwrap

import numpy as np
from PIL import Image, ImageFont, ImageDraw

import json
import os

# json_file = os.listdir("json")
# print(json_file)
from kakao_ocr import kakao_ocr_resize, kakao_ocr, kakao_translator


# 말풍선 좌표들의 최댓값, 최솟값을 구하는 함수 작성
def points(bubble_list: list):
    bubble_result = []
    for i in range(len(bubble_list)):
        tmp_bubble = np.array(bubble_list[i])
        tmp_min = np.min(tmp_bubble, axis=0)
        tmp_max = np.max(tmp_bubble, axis=0)
        x_min = tmp_min[0]
        y_min = tmp_min[1]
        x_max = tmp_max[0]
        y_max = tmp_max[1]

        bubble_result.append((x_min, y_min, x_max, y_max))
    return bubble_result


# 말풍선 이미지 크롭하는 함수
def crop_image(img_path: str, points: list, f_name: str):
    crop_paths = []
    for i in range(len(points)):
        img = Image.open(img_path)
        area = points[i]
        crop_img = img.crop(area)
        crop_path = './crop_images/crop_' + f_name + "_" + str(i) + ".jpg"
        crop_paths.append(crop_path)
        crop_img.save(crop_path)

    return crop_paths




# 카카오 ocr 사용하는 함수
def use_kakao_ocr(crop_path: str):
    appkey = "d1e155018697e1aa5510637a8554d043"

    resize_impath = kakao_ocr_resize(crop_path)
    if resize_impath is not None:
        crop_path = resize_impath
        print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr(crop_path, appkey).json()

    return output


# 카카오 ocr로 나온 text 데이터를 한 줄로 묶는 과정
# 텍스트 박스 좌표 지정
def text_recongition_words(ocr_data: dict):
    tmp_text = []
    tmp_box = []
    for i in range(len(ocr_data["result"])):
        tmp_text.append(ocr_data["result"][i]["recognition_words"][0])
        for j in range(len(ocr_data["result"][i]["boxes"])):
            tmp_box.append(ocr_data["result"][i]["boxes"][j])
    result_text = " ".join(tmp_text)

    tmp_box = np.array(tmp_box)
    r_min = np.min(tmp_box, axis=0)
    r_max = np.max(tmp_box, axis=0)

    return result_text, r_min, r_max


# 말풍선에 번역된 데이터를 넣기 위한 함수
def make_images(path: str, index: int, message: str, max_list: list, min_list: list):
    bg_color = 'white'

    font = ImageFont.truetype('./fonts/NanumGothic.ttf', size=10)
    # 글꼴 선택하게 해서 가능할듯
    font_color = 'black'

    w = max_list[0] - min_list[0]
    h = max_list[1] - min_list[1]

    image = Image.new('RGB', (w, h), color=bg_color)
    draw = ImageDraw.Draw(image)

    lines = textwrap.wrap(message, width=20)

    x_text = 0
    y_text = 0

    for line in lines:
        width, height = font.getsize(line)
        draw.text((x_text, y_text), line, font=font, fill=font_color)
        y_text += height


    make_images_path = "./make_images/" + path + "_" + str(index) + ".jpg"
    image.save(make_images_path)

    return make_images_path



# 말풍선에 결과 이미지 합성 함수
def paste_crop_image(f_name: str, index: int, crop_path: str, make_images_path: str, min_list: list):
    img1 = Image.open(crop_path)
    img2 = Image.open(make_images_path)

    start_point = (min_list[0], min_list[1])

    img1.paste(img2, start_point)
    path = "./result_crop_images/" + f_name + "_" + str(index) + ".jpg"
    img1.show()

    img1.save(path)

    return path




# result_crop_images_path 이미지를 원본 이미지에 붙여넣기
def paste_path(f_name:str, image_path: str, result_crop_images_path: str, bubble_point: tuple):
    img1 = Image.open(image_path)
    img2 = Image.open(result_crop_images_path)

    start_point = (int(bubble_point[0]), int(bubble_point[1]))

    img1.paste(img2, start_point)
    path = "./result_images/" + f_name + ".jpg"
    img1.save(path)
    img1.show()



def main():
    json_path = './json/00284.json'
    images_path = './images/00284.jpg'
    file_name = images_path.split('/')[-1].split('.')[0]
    print(file_name)
    # json 파일
    with open(json_path, 'r') as f:
        json_data = json.load(f)
        json_shape = json_data['shapes']

    # 하나의 이미지 파일 안에 있는 말풍선의 좌표들 저장
    bubble = []
    for i in range(len(json_shape)):
        if "bubble" in json_shape[i]['label']:
            # print(json_shape[i])
            bubble.append(json_shape[i]['points'])

    r_bubble = points(bubble)
    print(r_bubble[1])
    print(type(r_bubble[1]))
    print(r_bubble[1])

    crop_paths = crop_image(images_path, r_bubble, file_name)

    print(crop_paths)

    ocr_data = []
    for i in range(len(crop_paths)):
        ocr_data.append(use_kakao_ocr(crop_paths[i]))

    print(ocr_data[1])

    result_path = "./result_images/" + file_name + ".jpg"
    tmp_img = Image.open(images_path)
    tmp_img.save(result_path)

    for i in range(len(ocr_data)):
        result_text, min_list, max_list = text_recongition_words(ocr_data[i])
        trans_result = kakao_translator(result_text, 'en')[0]

        make_images_path = make_images(file_name, i, trans_result, max_list, min_list)


        print(result_text, min_list, max_list)


        result_crop_images_path = paste_crop_image(file_name, i, crop_paths[i], make_images_path, min_list)

        print(result_crop_images_path)

        paste_path(file_name, result_path, result_crop_images_path, r_bubble[i])

if __name__ == "__main__":
    main()