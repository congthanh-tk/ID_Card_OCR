import argparse
import time
import cv2
from cropper.cropper import crop_card
from detector.detector import detect_info, detect_info_CMTND
from reader import reader
import matplotlib.pyplot as plt
import numpy as np
import sys


def show_img(img):
    cv2.imshow('', img)
    cv2.waitKey(0)


def plot_img(img):
    plt.imshow(img)
    plt.show()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
ap.add_argument("-t", "--type", default='0',
                help="0: CCCD, 1: CMTND (card), 2: CMTND (giay)")
args = vars(ap.parse_args())


img = cv2.imread(args["image"])
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plot_img(img)

t1 = time.time()
warped = crop_card(args["image"])
# plot_img(warped)

if warped is None:
    print('Cant find id card in image')
    sys.exit()

# print("infor: ", len(detect_info(warped)))
try:
    if args["type"] == '0':
        # CCCD
        face, number_img, name_img, dob_img, gender_img, nation_img, \
            country_img, address_img, country_img_list, address_img_list = detect_info(
                warped)
        list_image = [face, number_img, name_img, dob_img,
              gender_img, nation_img, country_img, address_img]
    elif args["type"] == '1':
        # CMTND
        face, number_img, name_img, another_name_img, dob_img, gender_img, nation_img,  \
            country_img, address_img, country_img_list, address_img_list = detect_info_CMTND(
                warped)
        list_image = [face, number_img, name_img, dob_img,
              gender_img, nation_img, country_img, address_img]
    else:
        print("dang phat trien")
except:
    print('Cant find id card in image')
    sys.exit()

# print(list_image)

# for y in range(len(list_image)):
#     plt.subplot(len(list_image), 1, y+1)
#     plt.imshow(list_image[y])
# plt.show()

# from PIL import Image

# for img in list_image[1:]:
#     # print(img)
#     img = Image.fromarray(img)
#     plot_img(img)

#     s = detector.predict(img)
#     print(s)

# print(len(country_img_list), len(address_img_list))


number_text = reader.get_id_numbers_text(number_img)
name_text = reader.get_name_text(name_img)
# print(name_text)
dob_text = reader.get_dob_text(dob_img)
# print(dob_text)
gender_text = reader.get_gender_text(gender_img)
# print(gender_text)
nation_text = reader.get_nation_text(nation_img)
# print(nation_text)
country_text = reader.process_list_img(country_img_list, is_country=True)
# print(country_text)
address_text = reader.process_list_img(address_img_list, is_country=False)
# print(address_text)

texts = ['Số:'+number_text,
         'Họ và tên: ' + name_text,
         'Ngày tháng năm sinh: ' + dob_text,
         'Giới tính: ' + gender_text,
         'Quốc tịch: ' + nation_text,
         'Quê quán: ' + country_text,
         'Nơi thường trú: ' + address_text, " "]
t1 = time.time() - t1
print(t1)

plt.figure(figsize=(8, (len(texts) * 1) + 2))
plt.plot([0, 0], 'r')
plt.axis([0, 3, -len(texts), 0])
plt.yticks(-np.arange(len(texts)))
for i, s in enumerate(texts):
    plt.text(0.1, -i-1, s, fontsize=16)

plt.show()
