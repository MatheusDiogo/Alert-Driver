from machine import Pin
from umqtt.simple import MQTTClient
import network
import time

# Configura鑾借尗o do Wi-Fi
WIFI_SSID = 
WIFI_PASSWORD =

# Configura鑾借尗o do MQTT
MQTT_BROKER = "192.168.143.247"  # Endere鑾給 IP do broker MQTT
MQTT_PORT = 1883  # Porta padr鑼玱 para MQTT
MQTT_TOPIC_BUZZER = "esp32/buzzer/control"
MQTT_TOPIC_LED = "esp32/pisca_alerta/control"

# Configura鑾借尗o do buzzer
buzzer = Pin(23, Pin.OUT)

led = Pin(5, Pin.OUT)

led_state = False

def blink_led():
    global led_state
    led_state = not led_state
    led.value(led_state)
    time.sleep(0.1)

# Conectar ao Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Tentando conectar ao Wi-Fi...")
        time.sleep(1)
    print("Conectado ao Wi-Fi")
    print("IP:", wlan.ifconfig()[0])

# Fun莽茫o de callback para mensagens MQTT
def mqtt_callback(topic, msg):
    topic_str = topic.decode()  # Decodificar bytes para string
    msg_str = msg.decode()      # Decodificar bytes para string
    
    print("Recebido topico:", topic_str)
    print("Recebido mensagem:", msg_str)
    
    if topic_str == MQTT_TOPIC_BUZZER:
        if msg_str == "Dormindo":
            buzzer.value(1)  # Liga o buzzer
        elif msg_str == "Acordado":
            buzzer.value(0)  # Desliga o buzzer
    elif topic_str == MQTT_TOPIC_LED:
        if msg_str == "blink":
            blink_led()
        elif msg_str == "stop":
            led.value(0)
  
# Conectar ao broker MQTT
def connect_mqtt():
    client = MQTTClient("esp32_client", MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    try:
        client.connect()
        print("Conectado ao MQTT")
        client.subscribe(MQTT_TOPIC_BUZZER)
        client.subscribe(MQTT_TOPIC_LED)
    except OSError as e:
        print("Erro ao conectar ao MQTT:", e)
    return client

# Fun鑾借尗o principal
def main():
    connect_wifi()
    client = connect_mqtt()
    
    while True:
      try:
          client.check_msg()  # Espera por mensagens
      except OSError as e:
          print("Erro na comunicacao MQTT:", e)

if __name__ == "__main__":
    main()

