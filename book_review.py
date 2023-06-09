import cv2
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
cap = cv2.VideoCapture(0)

barcode_cnt = 0
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
