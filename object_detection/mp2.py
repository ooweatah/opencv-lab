import cv2
import time
import argparse
from multiprocessing import Process, Queue

# ... 이전 코드 생략 ...

# 객체 검출 함수 정의
def getObjects(q, img, thres, nms, draw=False, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence*100, 2)), (box[0]+200, box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    q.put((img, objectInfo))

if __name__ == "__main__":
    # 명령행 인수 처리
    parser = argparse.ArgumentParser()
    parser.add_argument("--thres", type=float, default=0.45, help="Confidence threshold for object detection")
    parser.add_argument("--nms", type=float, default=0.2, help="NMS threshold for object detection")
    args = parser.parse_args()

    # 비디오 캡처 객체 생성
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # 반복문을 이용한 객체 검출 시간 측정
    iterations = 10
    avg = []
    q = Queue() # 결과를 저장할 Queue 객체 생성

    while iterations > 0:
        start = time.time()
        success, img = cap.read()

        # 멀티프로세싱으로 객체 검출 함수 실행
        p = Process(target=getObjects, args=(q, img, args.thres, args.nms))
        p.start()
        p.join()

        # 객체 검출 결과를 가져와 이미지와 시간 출력
        img, objectInfo = q.get()
        end = time.time()
        loopTime = end - start
        print("thres={}, nms={}, each={}".format(args.thres, args.nms, loopTime))
        cv2.imshow("Output",img)
        cv2.waitKey(1)
        iterations -= 1
        avg.append(loopTime)

    print("thres={}, nms={}, avg={}".format(args.thres, args.nms, sum(avg) / len(avg)))
