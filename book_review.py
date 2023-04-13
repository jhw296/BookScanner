import cv2
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 바코드 인식
    barcodes = decode(frame)

    # 인식된 바코드가 있는 경우
    if len(barcodes) > 0:
        # 바코드 데이터 출력
        barcode_data = barcodes[0].data.decode("utf-8")
        print("Barcode data:", barcode_data)

        # ISBN 바코드인 경우 (978, 979로 시작하는 13자리 숫자)
        if (barcode_data.startswith("978") or barcode_data.startswith("979")) and len(barcode_data) == 13:
            # isbn = barcode_data[3:12]
            isbn = barcode_data
            # print(isbn)
            # 네이버 쇼핑에서 책 제목 검색
            url = f"https://search.shopping.naver.com/book/search?bookTabType=ALL&pageIndex=1&pageSize=40&query={isbn}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser') # html 파일
            # print(soup)
            title = soup.find('span', {'class':'bookListItem_text__bglOw'}).find('span').text

            if title is None:
                title = "Not Found"
            print("Title: ", title)
        else:
            print("Not an ISBN barcode")

    cv2.imshow('Barcode reader', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
