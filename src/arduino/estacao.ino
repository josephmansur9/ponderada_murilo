//esse código seria para o arduino UNO caso eu estivesse usando ele, ele envia um JSON pela porta Serial a cada 5 segundos

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;

void setup() {
  Serial.begin(9600);

  if (!bme.begin(0x76)) {
    Serial.println("BME280 nao encontrado. Verifique as conexoes.");
    while (1);
  }
}

void loop() {
  float temperatura = bme.readTemperature();          // °C
  float umidade     = bme.readHumidity();             // %
  float pressao     = bme.readPressure() / 100.0F;   // hPa

  Serial.print("{\"temperatura\":");
  Serial.print(temperatura, 2);
  Serial.print(",\"umidade\":");
  Serial.print(umidade, 2);
  Serial.print(",\"pressao\":");
  Serial.print(pressao, 2);
  Serial.println("}");

  delay(5000); // envia a cada 5 segundos, igual à simulação
}