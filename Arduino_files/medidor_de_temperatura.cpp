#include <math.h>

int analogPin = A3;
int val = 0;
float tensao_max = 5;
float r1 = 4600;
float ref = 5000;


float A_ = 3.354016e-03;
float B_ = 2.569850e-04;
float C_ = 2.620131e-06;
float D_ = 6.383091e-08;

float mede_tensao(int val) {
  float tensao = (val * 5.0) / 1023.0;
  return tensao;
}

float mede_res(float tensao) {
  float res = (tensao * r1) / (tensao_max - tensao);
  return res;
}

float mede_temp(float res) {
  float temp = pow(A_ + B_ * log(res / ref) + C_ * pow(log(res / ref), 2) + D_ * pow(log(res / ref), 3),-1)-273.15;
  return temp;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  val = analogRead(analogPin);
  Serial.print(val);
  Serial.print("\t");
  Serial.print(mede_tensao(val));
  Serial.print("\t");
  Serial.print(mede_res(mede_tensao(val)));
  Serial.print("\t");
  Serial.println(mede_temp(mede_res(mede_tensao(val))));
