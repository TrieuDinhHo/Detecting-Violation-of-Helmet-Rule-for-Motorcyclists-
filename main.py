import os
import socket
import datetime
import tempfile
import base64
import random
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from loguru import logger
from ultralytics import YOLO
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

	
app = FastAPI()

# Add CORS middleware for websever
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","*"],  # Adjust this to match your front-end origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

image_path = "./sample_image/"
output_dir = "./sample_image/output/"

color4cls0 = (255,0,0)
color4cls1 = (0,255,0)
color4cls2 = (0,0,255)
color4cls3 = (125,125,125)

model_selection_options = ['yolo-v8n-version1','yolov10n']
model_dict = {model_name: YOLO(f"./model_weight/{model_name}.pt") for model_name in model_selection_options}

logger.info("Init model success. Ready for predicting")
############################################
#---------GET Request Route----------------#
############################################
@app.get("/")
def root():
    return {"id": socket.gethostname()}

############################################
#---------POST Request Route---------------#
############################################

@app.post("/image")
async def simple_detect(file: UploadFile = File(...),
                        model_name: str = Form('yolo-v8n-version1')):
    # read imae from route 
    request_object_content = await file.read()
    # pil_image = Image.open(BytesIO(request_object_content))

    # Chuyển đổi nội dung thành mảng NumPy
    nparr = np.frombuffer(request_object_content, np.uint8)
    pil_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%Y%m%d_%H%M%S")
    logger.info("Predicting Image. Please wait...")
    
    results = model_dict[model_name].predict(source = pil_image,show=False) 

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

        cv2.rectangle(pil_image,start_point,end_point,color=color,thickness=2)

        cv2.putText(
            pil_image,
            str(name),
            (int(box[0]), int(box[1]) - 10),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.6,
            color = color,
            thickness=1
        )
    rand = random.randint(0,100000)
    file_dir = output_dir+f"file_{time_str}_{rand}.jpg"
    cv2.imwrite(file_dir, pil_image)
    logger.info(f"Output is saved in {file_dir}")
    return file_dir

@app.post("/video")
async def simple_detect(file: UploadFile = File(...),
                        model_name: str = Form('yolo-v8n-version1')):
    logger.info("Video Prediction is on going")
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%Y%m%d_%H%M%S")

    # Create a temporary file to save the uploaded video
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        video_path = tmp.name
    
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return {"error": "Could not open video."}

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Define the codec and create a VideoWriter object to save the processed video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = output_dir+f"{time_str}.mp4"
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reached the end of the video.")
            break

        results = model_dict[model_name].predict(source = frame,verbose=False) 
        frame = process_frame(frame,results)

        out.write(frame)

        # cv2.imshow('Processed Frame', processed_frame)

        # Wait for 25 ms and check if the user pressed 'q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    cap.release()
    out.release()

    rand = random.randint(0,100000)
    file_dir = output_dir+f"file_{time_str}_{rand}.mp4"
    logger.info(f"Output is saved in {file_dir}")

    return output_path

##############################################
#--------------Helper Functions---------------
##############################################
def process_frame(image, results):
    '''
    With results from yolo model, draw the bounding box of objects in that frame
    '''    
    # Extract bounding boxes, classes, names, and confidences
    boxes = results[0].boxes.xyxy
    classes = results[0].boxes.cls
    names = results[0].names
    confidences = results[0].boxes.conf

    for ids, box in enumerate(boxes):
        start_point = (int(box[0]), int(box[1]))
        end_point = (int(box[2]), int(box[3]))

        if int(classes[ids]) == 0:
            name = names[0]
            color = color4cls0
        elif int(classes[ids]) == 1:
            name = names[1]
            color = color4cls1
        elif int(classes[ids]) == 2:
            name = names[2]
            color = color4cls2
        elif int(classes[ids]) == 3:
            name = names[3]
            color = color4cls3

        cv2.rectangle(image, start_point, end_point, color=color, thickness=2)
        cv2.putText(
            image,
            str(name),
            (int(box[0]), int(box[1]) - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=color,
            thickness=3
        )
    return image
def list_folders(directory):
    # List all entries in the directory
    entries = os.listdir(directory)
    
    # Filter out directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
    
    return folders

def iter_videofile(file_path):
    """
    Show videos with input file_path
    """
    with open(file_path, mode="rb") as file_like:  
        yield from file_like 

def results_to_json(results, model):
    ''' Converts yolo model output to json (list of list of dicts)'''
    # Extract bounding boxes, classes, names, and confidences
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()
    
    results_json = []
    for bb, clss, conf in zip(boxes, classes, confidences):
        result_dict = {
            'bboxes': bb,
            'classes': clss,
            'probs': conf
        }
        results_json.append(result_dict)
    
    return [results_json]

def base64EncodeImage(img):
    ''' Takes an input image and returns a base64 encoded string representation of that image (jpg format)'''
    _, im_arr = cv2.imencode('.jpg', img)
    im_b64 = base64.b64encode(im_arr.tobytes()).decode('utf-8')

    return im_b64

def plot_one_box(x, im, color=(128, 128, 128), label=None, line_thickness=3):
    # Directly copied from: https://github.com/ultralytics/yolov5/blob/cd540d8625bba8a05329ede3522046ee53eb349d/utils/plots.py
    # Plots one bounding box on image 'im' using OpenCV
    assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image.'
    tl = line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(im, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(im, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
