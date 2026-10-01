import cv2

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Couldn't connect to camera")
    while True:
        success, frame = cap.read()
        cv2.imshow("Test", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            return

main()