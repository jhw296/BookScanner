import cv2
import requests
import os
import numpy as np
import pytesseract
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image

def text_extraction():
    def draw_rect(img):
        rois = [(p-small, small * 2) for p in pts1]
        for (x, y), (w, h) in np.int32(rois):
            roi = img[y:y + h, x:x + w]                 # 좌표 사각형 범위 가져오기
            val = np.full(roi.shape, 80, np.uint8)  # 컬러(3차원) 행렬 생성		cv2.add(roi, val, roi)                      			# 관심영역 밝기 증가
            cv2.add(roi, val, roi)
            cv2.rectangle(img, (x, y, w, h), (255, 255, 255), 1)
        cv2.polylines(img, [pts1.astype(int)], True, (0, 255, 0), 1)     # pts는 numpy 배열
        cv2.imshow("select rect", img)
        

    def warp(img):
        global roi_image, flag
        perspect_mat = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, perspect_mat, (500, 100), cv2.INTER_CUBIC)
        roi_image = img_contrast(dst)
        cv2.imshow("perspective transform", dst)
        cv2.imshow("test", roi_image)
        
        image_pdf = Image.fromarray(roi_image)
        image_pdf = image_pdf.convert('RGB')
        image_pdf.save('./img/pdf_image.pdf')
        
        if flag == 1:
            test = pytesseract.image_to_string(roi_image, lang='eng')
            # test = pytesseract.image_to_string(roi_image, lang='kor')
            print('roi : ', test)
            

    def img_contrast(img):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
        return final
    
    
    def onMouse(event, x, y, flags, param):
        global check, roi_image, flag
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, p in enumerate(pts1):
                p1, p2 = p - small, p + small           # p점에서 우상단, 좌하단 좌표생성
                if contain_pts((x, y), p1, p2): check = i

        if event == cv2.EVENT_LBUTTONUP: check = -1                                  # 좌표 번호 초기화
        
        if event == cv2.EVENT_LBUTTONDOWN:
            flag = 1
            
        if check >= 0 :                                 # 좌표 사각형 선택 시
            pts1[check] = (x, y)
            draw_rect(np.copy(image))
            warp(np.copy(image))
            
            
    def contain_pts(p, p1, p2):
        return p1[0] <= p[0] < p2[0] and p1[1] <= p[1] < p2[1]
    
    global check, roi_image, flag
    small = np.array((12, 12))                                    # 좌표 사각형 크기
    check = -1                                          # 선택 좌표 사각형 번호 초기화
    width = 600
    height = 400
    pts1 = np.float32([(100, 100), (300, 100), (300, 300), (100, 300)])
    pts2 = np.float32([(0, 0), (500, 0), (500, 100), (0, 100)])  # 목적 영상 4개 좌표

    image = np.empty([])
    roi_image = np.empty([])
    flag = 0
    
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()
        # print(type(frame), len(frame))
        if not ret:
            continue

        cv2.imshow('text reader', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            image = frame
            # print(image)
            break
            
    cap.release()
    # cv2.imshow('image', image)
    cv2.destroyAllWindows()
    draw_rect(np.copy(image))
    cv2.setMouseCallback("select rect", onMouse, 0)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()