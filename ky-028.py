from machine import Pin, ADC, I2C
import ssd1306
from time import sleep
import network
from umqtt.simple import MQTTClient

# Configuración de pines
PIN_SENSOR_SONIDO_ANALOGICO = 34  # Por ejemplo, puedes usar el pin 34 de la ESP32

# Inicialización del ADC
adc = ADC(Pin(PIN_SENSOR_SONIDO_ANALOGICO))
adc.atten(ADC.ATTN_11DB)  # Configurar la atenuación para un rango más amplio de medición (dependiendo de tu módulo ESP32)

# Configuración del I2C para la pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

MQTT_BROKER = "192.168.43.135"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/dal/ky-028"
MQTT_PORT = 1883

# Umbral para determinar si hay sonido o no
UMBRAL_SONIDO = 3000  # Ajustar este valor según las pruebas y la sensibilidad deseada

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Adrian', '123456ad')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi Conectada!")

def display_value(value):
    oled.fill(0)  # Limpiar pantalla
    oled.text("Temperatura detectado:", 0, 0)
    oled.text(str(value), 0, 20)
    oled.show()

def publicar_mensaje(msg):
    client.publish(MQTT_TOPIC, msg)

def verificar_funcionamiento():
    while True:
        valor_analogico = adc.read()
        valor_enviar = 1 if valor_analogico >= UMBRAL_SONIDO else 0
        publicar_mensaje(str(valor_enviar))  # Publicar 1 o 0
        print(valor_enviar)
        display_value(valor_enviar)
        sleep(15)
        

# Bucle principal
print('Programa iniciado. Presiona CTRL+C para salir.')
conectar_wifi()
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
client.connect()

verificar_funcionamiento()
