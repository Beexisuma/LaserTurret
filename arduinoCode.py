import cv2
import serial
import time
from ultralytics import YOLO

# === CONFIG ===
PORT = "COM5"  
BAUD = 115200
MODEL_PATH = "runs/detect/bestOne.pt"  # Custom Model
CONF = 0.3
CAM_INDEX = 0

# === SERIAL ===
arduinoData = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)  #

# === CAMERA ===
cap = cv2.VideoCapture(CAM_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# === YOLO ===
model = YOLO(MODEL_PATH)

def send_to_arduino(cx, cy, frame_w, frame_h):
    dx = int(cx - frame_w / 2)
    dy = int(cy - frame_h / 2)
    msg = f"CX:{int(cx)},CY:{int(cy)},DX:{dx},DY:{dy}\n"
    arduinoData.write(msg.encode("utf-8"))
    print("Sent ->", msg.strip())

def pick_best_box(result):
    boxes = result.boxes
    if boxes is None or boxes.xywh is None or len(boxes) == 0:
        return None
    xywh = boxes.xywh.cpu().numpy()
    confs = boxes.conf.cpu().numpy()
    i = confs.argmax()
    cx, cy, w, h = xywh[i, :4]
    return float(cx), float(cy), float(confs[i])

while True:
    ok, frame = cap.read()
    if not ok:
        break

    H, W = frame.shape[:2]

    # Run detection
    results = model.track(frame, conf=CONF, tracker='bytetrack.yaml',)
    r = results[0]

    choice = pick_best_box(r)
    if choice:
        cx, cy, conf = choice

        # send to Arduino
        send_to_arduino(cx, cy, W, H)
        print(cx,cy,W,H)

        # visualize
        cv2.circle(frame, (int(cx), int(cy)), 6, (255, 255, 0), -1)

    # draw frame center crosshair
    cv2.drawMarker(frame, (W//2, H//2), (255, 255, 255),
    markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    cv2.imshow("YOLOv11 -> Arduino (center send)", frame)
    if cv2.waitKey(1) & 0xFF in (ord('q'), ord('d')):
        break

cap.release()
arduinoData.close()
cv2.destroyAllWindows()
