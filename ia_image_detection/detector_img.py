from ultralytics import YOLO
import cv2


model = YOLO("C:/Users/natha/Stockage/programmation/ia_image_detection/runs/detect/train3/weights/last.pt")
threshold = 0.5



ret, frame = ......read
if not ret:
    print("Erreur lors de la capture de la caméra.")
    break

results = model(frame)[0]

for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        height = y2 - y1
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, results.names[int(class_id)].upper(), 
                        (int(x1), int(y1) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1.0, (0, 255, 0), 2)
    
cv2.imshow("Camera", frame)

height = y2 - y1

cv2.destroyAllWindows()