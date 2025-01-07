import threading
import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker="test.mosquitto.org", port=1883, topic="data/weight"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.latest_message = None

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado ao broker MQTT com código de retorno {rc}")
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            import json
            self.latest_message = json.loads(msg.payload.decode())
            print(f"Mensagem recebida: {self.latest_message}")
        except json.JSONDecodeError:
            print("Erro ao decodificar mensagem JSON")

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def get_latest_message(self):
        return self.latest_message
