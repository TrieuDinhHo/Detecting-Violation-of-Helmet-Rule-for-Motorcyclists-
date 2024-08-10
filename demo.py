import cv2
import tempfile
from ultralytics import YOLO
from loguru import logger

# Load a pre-trained YOLO model
model = YOLO("./model_weight/yolo-v8n-version1.pt")
logger.info("Init model success. Ready for predicting")

color4cls0 = (255,0,0)
color4cls1 = (0,255,0)
color4cls2 = (0,0,255)
color4cls3 = (125,125,125)

image = cv2.imread("./sample_image/xemay.jpeg")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = model.predict(source = 'sample_image/xemay.jpeg',show=False) # camera

# Extract bounding boxes, classes, names, and confidences
boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

results = {"bboxes": boxes, "classes": classes, "probs": confidences}

# Iterate through the results
for ids,box in enumerate(results['bboxes']):
    start_point = (int(box[0]), int(box[1]))
    end_point = (int(box[2]), int(box[3]))

    if int(results["classes"][ids]) == 0:
        name = names[0]
        color = color4cls0
    elif int(results["classes"][ids]) == 1:
        name = names[1]
        color = color4cls1
    elif int(results["classes"][ids]) == 2:
        name = names[2]
        color = color4cls2
    elif int(results["classes"][ids]) == 3:
        name = names[3]
        color = color4cls3

    cv2.rectangle(image,start_point,end_point,color=color,thickness=2)

    cv2.putText(
        image,
        str(name),
        (int(box[0]), int(box[1]) - 10),
        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
        fontScale = 0.6,
        color = color,
        thickness=1
    )
cv2.imwrite("./sample_image/output/xemay.jpg", image)
