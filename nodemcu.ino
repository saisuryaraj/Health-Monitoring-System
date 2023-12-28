#include<Wire.h>
#include <FirebaseESP8266.h>  
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>

#define FIREBASE_HOST "health-monitoring-e687e-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "AIzaSyB5NuRkoLkJHoh1pG7-wlv1-a60ex2ZM2Q"
#define WIFI_SSID "nodemcu1"
#define WIFI_PASSWORD "nodemcu1"

FirebaseData firebaseData;
FirebaseJson json;

void setup() {
  Wire.begin();
  Serial.begin(9600);

  wifiConnect();

  Serial.println("Connecting Firebase.....");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
  Serial.println("Firebase OK.");
}

void wifiConnect()
{
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
}

void loop() {
  Wire.requestFrom(2,20);
  String string,string1,string2;
  do
  {
    char c = Wire.read();
    string = string+c;
    string1 = string.substring(0,4);
    string2 = string.substring(5);
    
    Serial.println(string);
//    Serial.println(string1);
//    Serial.println(string2);

  } while (Wire.available());
  
  char buf1[10];
  char buf2[10];

  string1.toCharArray(buf1, 10);
  long tem = atol(buf1);
  float temp = tem*0.01;
  Serial.println(temp);

  string2.toCharArray(buf2, 10);
  int pulse = atoi(buf2);
  Serial.println(pulse);

  Firebase.setFloat(firebaseData,"healthuuu/Temperature",temp);
  Firebase.setFloat(firebaseData,"health/Pulserate",pulse);

}
