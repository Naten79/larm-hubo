from ultralytics import YOLO
import cv2

# Initialisation de la capture de la caméra
cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera")

# Chargement du modèle YOLO
model = YOLO("C:/Users/natha/Stockage/programmation/ia_image_detection/runs/detect/train3/weights/last.pt")
threshold = 0.5

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Erreur lors de la capture de la caméra.")
        break
    
    # Détection des objets dans l'image
    results = model(frame)[0]
    
    # Dessiner les boîtes englobantes et les étiquettes
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, results.names[int(class_id)].upper(), 
                        (int(x1), int(y1) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1.0, (0, 255, 0), 2)
    # Affichage du résultat
    cv2.imshow("Camera", frame)
    
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération des ressources
cam.release()
cv2.destroyAllWindows()





