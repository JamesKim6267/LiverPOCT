import cv2
import numpy as np
from PIL import Image,ImageEnhance
import matplotlib.pyplot as plt
from io import BytesIO
import requests

import streamlit as st

#rgb_img = rgb색을 가지는 opencv용 사진파일
#
def binary(color_img):
    lower = np.array([0,0,0])
    higher = np.array([280,200,200])
    binary_img = cv2.inRange(color_img,lower,higher)
    return binary_img

def contour(binary_img):
    cont,_ = cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cont_img = cv2.drawContours(rgb_image,cont,-1,255,3)
    c = max(cont,key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(rgb_image,(x,y),(x+w,y+h),(0,255,0),5) 
    cropped_img = rgb_image_copy[y:y+h,x:x+w]
    return cropped_img

def average_rgb(cropped_img):
     average_color_row = np.average(cropped_img,axis = 0)
     average_color = np.average(average_color_row, axis = 0)
     Red,Green,Blue = average_color
     return Red,Green,Blue 

def ALT(Red,Green):
    if 185 <= Green <= 194: #ALT Range 0-40
        alt_level_R = 8*Red - 1600
        alt_level_G = -4.4444*Green + 862.22
        alt= (alt_level_R + alt_level_G)/2
    if 168 <= Green <= 184: #ALT Range 40-60
        alt_level_R = -1.5385*Red + 355.38
        alt_level_G = -1.1765*Green + 257.65
        alt = (alt_level_R + alt_level_G)/2
    if 136 <= Green <= 167: #ALT Range 60-180
        alt_level_R =  -5.3555*Red + 1101.9
        alt_level_G = -2.9914*Green + 577.21
        alt = (alt_level_R + alt_level_G)/2
    if 108 <= Green <= 135: #ALT Range 180-200
         alt_level_R = -1.3333*Red + 414.67
         alt_level_G =  -0.7145*Green + 277.14
         alt = (alt_level_R + alt_level_G)/2
    if 89 <= Green <= 107: #ALT Range 200-300
         alt_level_R = -5.9701*Red + 1157.5
         alt_level_G =  -5.2583*Green + 768.82
         alt = (alt_level_R + alt_level_G)/2
    if Green <=88 or Green >=195:
        st.write('Wrong image file, Please try again')
    return alt




     

st.title("ALT&AST Level Detection")
aminase = ['ALT','AST']
if st.button("ALT Read Guide"):
    st.write("Normal: 0~40U/L")
    st.write("Slight Abnormal: 40~120U/L")
    st.write("Serious Abnormal: 120U/L~")
if st.button("AST Read Guide"):
    st.write("Normal: 0~41U/L")
    st.write("Slight Abnormal: 41~100U/L")
    st.write("Serious Abnormal: 100U/L~")
selected_aminase = st.selectbox('Select your test type',aminase)
uploaded_file = st.file_uploader("Choose an image file", type=['jpg','jpeg','png'])

if uploaded_file is not None and selected_aminase == 'ALT':
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    rgb_image = cv2.cvtColor(opencv_image,cv2.COLOR_BGR2RGB)
    rgb_image_copy = rgb_image.copy()
    st.image(rgb_image)
    if st.button("Process"): 
        color_img = rgb_image
        binary_img = binary(color_img)
        if binary_img is not None: 
            cropped_img = contour(binary_img)
            st.image(cropped_img)
            if cropped_img is not None:
                Red,Green,Blue = average_rgb(cropped_img)
                if Red and Green is not None:
                    alt_level = ALT(Red,Green)
                    if alt_level <= 20:
                        st.write("ALT Range: 0-20U/L")
                    if alt_level >20 and alt_level <=40:
                        st.write("ALT Range: 20-40U/L")
                    if alt_level >40 and alt_level <=60:
                        st.write("ALT Range: 40-60U/L")
                    if alt_level >60 and alt_level <=80:
                        st.write("ALT Range: 60-80U/L")
                    if alt_level >80 and alt_level <=100:
                        st.write("ALT Range: 80-100U/L")
                    if alt_level >100 and alt_level <=120:
                        st.write("ALT Range: 100-120U/L")
                    if alt_level >120 and alt_level <=140:
                        st.write("ALT Range: 120-140U/L")
                    if alt_level >140 and alt_level <=200:
                        st.write("ALT Range: 140-200U/L")
                    if alt_level > 200:
                        st.write("ALT Range > 200U/L")


if uploaded_file is not None and selected_aminase == 'AST':
    st.write('This service is not ready')
