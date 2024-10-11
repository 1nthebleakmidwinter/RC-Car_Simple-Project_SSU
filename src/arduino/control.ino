#include <Servo.h>
#define motorPin1 2
#define motorPin2 4
#define servoPin 9
#define trigPin 6
#define echoPin 5
Servo myservo;
int emergency2 = 1;
byte commands[4] = {0x00,0x00,0x64,0x00};
char trash[10] = {0,};
void setup()
{   
  Serial.begin(9600);
  pinMode(motorPin1,OUTPUT);
  pinMode(motorPin2,OUTPUT);
  myservo.attach(servoPin);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop()
{
  if(Serial.available()==4)
  { 
    emergency2 = 1;
    commands[0] = Serial.read();  //Direction
    commands[1] = Serial.read();  
    commands[2] = Serial.read();  //Angle
    commands[3] = Serial.read();  
    
    if(commands[0] == 0xf1)
    {
      digitalWrite(motorPin1,HIGH);
      digitalWrite(motorPin2,LOW);
      myservo.write(commands[2]);
    }
    if(commands[0] == 0xf2)
    {
      digitalWrite(motorPin1,LOW);
      digitalWrite(motorPin2,HIGH);
      myservo.write(commands[2]);
    }
    if(commands[0] == 0xf3)
    {
      digitalWrite(motorPin1,LOW);
      digitalWrite(motorPin2,LOW);
      myservo.write(commands[2]);
    }
  }
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  int distance = (duration * 0.0343) / 2;
  Serial.write(itoa(distance, trash, 10));
  delay(5);
  if((distance < 10)&&(commands[0] != 0xf2)&&(commands[1]==0xff)&&(emergency2 == 1))
  {
    digitalWrite(motorPin1,LOW);
    digitalWrite(motorPin2,HIGH);
    delay(15);
    digitalWrite(motorPin1,LOW);
    digitalWrite(motorPin2,LOW);
    emergency2 = 0;
  }
}
