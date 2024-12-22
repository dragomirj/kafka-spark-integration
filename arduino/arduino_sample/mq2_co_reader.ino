//DJ - MQ-2 Sensor for LPG & CO
#include <MQ2.h>
int pin = A3;  //The Arduino pin to which the AOUT of the MQ-2 sensor is connected to
float lpg, co; //LPG (Liquefied Petroleum Gas) & CO (Carbon monoxide)

//INITIALIZE MQ2 LIBRARY
MQ2 mq2(pin);

void setup(){
  Serial.begin(9600);
  pinMode(pin, INPUT);
  mq2.begin(); //Sensor Calibration
} //SETUP

void loop(){
  lpg = mq2.readLPG();
  co  = mq2.readCO();
  Serial.println(co); //Serial output is read by Raspberry Pi
} //LOOP