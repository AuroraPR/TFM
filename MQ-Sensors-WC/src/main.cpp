#include <PubSubClient.h>
#include <ESP8266WiFi.h>

int gas_sensor = A0;                      //Sensor pin
float m = -0.263;                         //Slope
float b = 0.42;                           //Y-Intercept
float R0 = 2.77;                          //Sensor Resistance in fresh air from previous code
float sensor_volt;                        //Define variable for sensor voltage
float RS_gas;                             //Define variable for sensor resistance
float ratio;                              //Define variable for ratio
float sensorValue;                        //get value from sensor
double ppm_log;                           //Get ppm value in linear scale according to the the ratio value
double ppm;                               //Convert ppm value to log scale

const char* ssid     = "Adetem";
const char* password = "AuroraJavi";

const char* topic = "sensors/mq137";
const char* server = "192.168.31.199";

void callback(char* topic, byte* payload, unsigned int length) {
}

WiFiClient wifiClient;
PubSubClient client(server, 1883, callback, wifiClient);


String macToStr(const uint8_t* mac)
{
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    if (i < 5)
      result += ':';
  }
  return result;
}

void setup() {
  Serial.begin(9600); //Baud rate
  delay(10);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  String clientName;
  clientName += "esp8266-";
  uint8_t mac[6];
  WiFi.macAddress(mac);
  clientName += macToStr(mac);
  clientName += "-";
  clientName += String(micros() & 0xff, 16);



  if (client.connect((char*) clientName.c_str())) {
    Serial.println("Connected to MQTT broker");
  } else {
  Serial.println("MQTT connect failed");
    abort();
  }
}

void calculate_ppm() {
  sensorValue = analogRead(gas_sensor); //Read analog values of sensor
  sensor_volt = sensorValue * (5.0 / 1023.0); //Convert analog values to voltage
  RS_gas = ((5.0 * 10.0) / sensor_volt) - 10.0; //Get value of RS in a gas
  ratio = RS_gas / R0; // Get ratio RS_gas/RS_air

  //convert to ppm value//
  ppm_log = (log10(ratio) - b) / m;
  ppm = pow(10, ppm_log);

  //display value//
  Serial.print("Ammonia: ");
  Serial.println(ppm);

  String buf;
  buf+=String(sensorValue);
  buf+=String("@");
  buf+=String(ppm);
  client.publish(topic, buf.c_str());

  delay(255);
}

void loop(){
  calculate_ppm();

}
