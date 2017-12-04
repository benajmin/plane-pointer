/*  Plane Pointer
    Benjamin Wilkins
    December 3, 2017

    Requires LCD I2C library
    https://bitbucket.org/fmalpartida/new-liquidcrystal/downloads
*/

#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define YAW_SERVO_PIN 5
#define PITCH_SERVO_PIN 6
#define INTERVAL 3000

void displayPlane();

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

Servo yaw_servo;
Servo pitch_servo;

String serialData;

String model;
String op;
String to;
String from;
unsigned int alt;
float dist;

byte arrow[8] = {
  B00000,
  B00100,
  B00010,
  B11111,
  B00010,
  B00100,
  B00000,
  B00000
};

void setup() {
  yaw_servo.attach(YAW_SERVO_PIN);
  pitch_servo.attach(PITCH_SERVO_PIN);

  Serial.begin(9600);
  
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.createChar(0, arrow);

  lcd.setCursor(0, 0);
  lcd.print("Plane Pointer");
  lcd.setCursor(0, 1);
  lcd.print("Benjamin Wilkins");

  // Point "North"
  yaw_servo.write(0);
  pitch_servo.write(0);
  delay(5000);
}

unsigned long previousMillis =  millis();
int state = 0;

void loop() {
  // put your main code here, to run repeatedly:

  if (millis() - previousMillis > INTERVAL){
    previousMillis = millis();
    state = (state + 1) % 3;
    displayPlane();
  }
}

void serialEvent() {
  serialData = Serial.readString();
  model = parse(serialData, "<Mdl>", "<");
  op = parse(serialData, "<Op>", "<");
  to = parse(serialData, "<To>", "<");
  from = parse(serialData, "<From>", "<");

  alt =  parse(serialData, "<GAlt>", "<").toInt();
  dist =  parse(serialData, "<Dst>", "<").toFloat();

  int pitch = parse(serialData, "<Pitch>", "<").toInt();
  int yaw = parse(serialData, "<Yaw>", "<").toInt();

  if (yaw < 0){
    yaw *= -1;
  }else{
    yaw = 180 - yaw;
    pitch = 180 - pitch;
  }

  yaw_servo.write(yaw);
  pitch_servo.write(pitch);
}

String parse (String input, String d1, String d2){
  int start = input.indexOf(d1) + d1.length();
  int finish = input.indexOf(d2, start) + d2.length();
  return input.substring(start, finish-1);
}

void displayPlane(){
  lcd.clear();
  lcd.setCursor(0,0);

  switch (state) {
    case 0:
      if (to.length() != 0 && from.length() != 0){
        lcd.print(from);
        lcd.write(byte(0)); //arrow
        lcd.print(to);
        break;
      }
    case 1: 
      if (model.length() != 0){
        lcd.print(model);
        break;
      }
    case 2:
      if (op.length() != 0){
        lcd.print(op);
        break;
      }
    default: 
      lcd.print("Plane Pointer");
      break;
  }
  
  lcd.setCursor(0, 1);
  lcd.print(dist);
  lcd.print("km");
  lcd.setCursor(8, 1);
  lcd.print(alt);
  lcd.print("ft");
}

