import time
from keras.models import load_model
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

# MQTT configuration
MQTT_BROKER = "localhost"  # Broker address
MQTT_PORT = 1883  # Broker port
MQTT_TOPIC = "buzzer/control"  # Topic for buzzer control

# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

despertar = 0

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index].strip().split(' ')[1]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name, end="\n")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
    
    if(class_name == 'Dormindo'):
        despertar += 1
        
        if despertar >= 20:
            #enviar informação para o buzzer ligar
            mqtt_client.publish(MQTT_TOPIC, "Dormindo")
    
    else:
        despertar = 0
        #enviar informação para o buzzer parar
        mqtt_client.publish(MQTT_TOPIC, "Acordado")

    time.sleep(0.1)

camera.release()
cv2.destroyAllWindows()