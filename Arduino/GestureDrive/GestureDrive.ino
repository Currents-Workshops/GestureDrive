//Include necessary libraries
#include <Servo.h>
#include<SoftwareSerial.h>

//Define motor driver and servo pins
#define IN1 2
#define IN2 3
#define IN3 4
#define IN4 5
#define ServoPin 8
const int trigPin = 9;  // Trigger pin
const int echoPin = 10; // Echo pin

Servo myservo; //declare object of servo class
SoftwareSerial bt(6,7); //declare object of SoftwareSerial class (6-Rx , 7-Tx)

void setup() {

//Set motor driver pins as output
pinMode(IN1,OUTPUT);
pinMode(IN2,OUTPUT);
pinMode(IN3,OUTPUT);
pinMode(IN4,OUTPUT);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);

myservo.attach(ServoPin); //Attach servo pin to servo object

Serial.begin(9600); //Set baud rate for serial communication using USB
bt.begin(9600); //Set baud rate for serial communication using Bluetooth Module

}

char t; //String to read input from bluetooth comm

//Both motors move forward
void forward()
{
digitalWrite(IN1,0);
digitalWrite(IN2,1);
digitalWrite(IN4,0);
digitalWrite(IN3,1);
}

//Both motors move backwards
void reverse()
{
digitalWrite(IN1,1);
digitalWrite(IN2,0);
digitalWrite(IN4,1);
digitalWrite(IN3,0);
}

//Only left motor rotates
void right()
{
digitalWrite(IN1,0);
digitalWrite(IN2,0);
digitalWrite(IN4,0);
digitalWrite(IN3,1);
}

//Only right motor rotates
void left()
{
digitalWrite(IN1,0);
digitalWrite(IN2,1);
digitalWrite(IN3,0);
digitalWrite(IN4,0);
}

//All motor stops
void brake()
{
digitalWrite(IN1,0);
digitalWrite(IN2,0);
digitalWrite(IN3,0);
digitalWrite(IN4,0);
}



void loop() {

//Read if data is available
if(bt.available())
{
  t = bt.readString()[0];
  Serial.println(t);
  if(t == 'F')
  forward();
  else if(t == 'B')
  reverse();
  else if(t == 'L')
  left();
  else if(t == 'R')
  right();
  else if(t == 'S')
  brake();
  else if(t == 'N')
  {
    brake();
    char Data[800];
    for(int i =0 ; i < 800 ; i++) Data[i] = ' ';
    int index = 0;
    for (int i = 0; i <= 180; i++) {
      
      myservo.write(i);  // Set the servo angle
      delay(50);  // Delay for smooth motion
      String data = String(readUltrasonicSensor())+" ";
      for(int j = 0 ; j < data.length() ;j++)
      {
        Data[index] = data[j];
        index++;
      }
    }
    Data[799] = '\0';
    bt.print(Data);
//    Serial.println(Data);
    myservo.write(0);
    delay(1000);
  }
}

//delay(100);
}

int readUltrasonicSensor() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int cm = duration / 58; // Convert the time to distance in centimeters

  return cm;
}
