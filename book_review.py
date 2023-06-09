import cv2
import requests
import os
import numpy as np
# import pytesseract import Output
import pytesseract
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image


def main():
    # barcorde_recognition()
    text_extraction()

def barcorde_recognition():
    load_dotenv()
    barcode_cnt = 0
    
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray) # 바코드 인식

        for barcode in barcodes:
            barcode_cnt += 1
            x, y, w, h = barcode.rect
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            barcode_text = '%s (%s)' % (barcode_data, barcode_type)
            
            # print("Barcode data:", barcode_data)
            
            # barcode bounding box 생성
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, barcode_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

            # ISBN 바코드인 경우 (978, 979로 시작하는 13자리 숫자)
            if (barcode_data.startswith("978") or barcode_data.startswith("979")) and len(barcode_data) == 13:
                isbn = barcode_data
                key = os.environ.get('key')
                url = f"https://www.nl.go.kr/NL/search/openApi/search.do?key={key}&detailSearch=true&isbnOp=isbn&isbnCode={isbn}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser') # html 파일
                
                title = soup.find('title_info').text

                if title is None:
                    title = "Not Found"
                    
                # 바코드가 지속적으로 10번 이상 감지될 경우 해당 도서 정보 출력
                if barcode_cnt >= 10:
                    path = './img/snapshot_' + str(title) + '.jpg'
                    cv2.imwrite(path, frame)
                    cap.release()
                    print("Title: ", title)
                    
            else:
                print("Not an ISBN barcode")

        cv2.imshow('Barcode reader', frame)
        # cv2.imshow('grayscale', gray) 
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
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
    
if __name__ == '__main__':
    main()
