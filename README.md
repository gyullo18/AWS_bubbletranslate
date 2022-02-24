# AWS_bubbletranslate
main.py
-------------------------------------------------------------------------------------------------------------
def points(bubble_list: list):

말풍선 좌표들을 입력받아 x, y 좌표의 최댓값과 최솟값을 구하는 함수
def crop_image(img_path: str, points: list, f_name: str):

이미지 주소, 말풍선 좌표, 파일이름(ex: 12345.jpg -> 12345)들을 입력받아 말풍선 좌표들에 해당하는 부분을 crop하는 함수
def use_kakao_ocr(crop_path: str):

카카오 ocr api를 사용하는 함수
def text_recognition_words(ocr_data: dict):

카카오 ocr api를 이용하여 나온 결과를 정리하여 text 데이터들을 한 줄로 묶고, text 데이터가 나온 x, y좌표의 최댓값과 최솟값을 구하는 함수
def make_images(path: str, index: int, message: str, max_list: list, min_list: list):

말풍선에 변역 결과를 넣을 텍스트 이미지를 만들기 위한 과정
def paste_crop_image(f_name: str, index: int, crop_path: str, make_images_path: str, min_list):

crop된 말풍선 이미지에 번역된 텍스트 이미지를 넣는 함수
def paste_path(f_name: str, image_path: str, result_crop_images_path: str, bubble_point: tuple):

번역된 텍스트 이미지를 붙여넣은 말풍선 이미지를 원래 말풍선 자리에 붙여 넣는 함수
