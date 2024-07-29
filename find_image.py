import cv2
import pyautogui as pg
import numpy as np
import time

def preprocess_image(image):
    # แปลงเป็นภาพขาวดำ
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ใช้ GaussianBlur เพื่อลดสัญญาณรบกวนและเพิ่มความแม่นยำในการตรวจจับ
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # ใช้การตรวจจับขอบ Canny
    edges = cv2.Canny(blurred, 50, 150)
    return edges

while True:
    print("Looking for image...")  
    # อ่านภาพเข็มและเตรียมภาพล่วงหน้า
    needle = cv2.imread('bg.png')
    needle_preprocessed = preprocess_image(needle)
    
    # จับภาพหน้าจอและเตรียมภาพล่วงหน้า
    screenshot = pg.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    haystack_preprocessed = preprocess_image(screenshot)
    
    # ทำการจับคู่เทมเพลตโดยใช้ขอบ
    result = cv2.matchTemplate(haystack_preprocessed, needle_preprocessed, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    
    # สร้างสำเนาภาพหน้าจอเพื่อวาดกรอบสี่เหลี่ยม
    screenshot_copy = screenshot.copy()
    
    # ตรวจสอบว่าพบภาพหรือไม่
    if len(loc[0]) > 0:
        print("Found images!")
        for pt in zip(*loc[::-1]):  # สลับตำแหน่ง x, y
            x, y = pt
            w, h = needle.shape[1::-1]
            # แคปเจอร์เฉพาะบริเวณที่ตรวจจับได้
            detected_region = screenshot[y:y + h, x:x + w]
            # วาดกรอบสี่เหลี่ยมรอบภาพที่พบ
            cv2.rectangle(screenshot_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # แสดงผลลัพธ์
            cv2.imshow('Detected Region', detected_region)
            cv2.waitKey(500)  # แสดงภาพเป็นเวลา 0.5 วินาที (500 มิลลิวินาที)
            cv2.destroyWindow('Detected Region')  # ปิดหน้าต่างที่แสดงผล
        # แสดงภาพหน้าจอที่มีกรอบสี่เหลี่ยมรอบภาพที่พบทั้งหมด
        cv2.imshow('Detected Regions', screenshot_copy)
        cv2.waitKey(500)  # แสดงภาพเป็นเวลา 0.5 วินาที (500 มิลลิวินาที)
        cv2.destroyWindow('Detected Regions')  # ปิดหน้าต่างที่แสดงผล
    else:
        print("Image not found.") 
    
    time.sleep(1)  # รอ 1 วินาที ก่อนตรวจสอบใหม่อีกครั้ง
