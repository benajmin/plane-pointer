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

char model[17] = "2010 CESSNA 525A";
char op[17] = "DELTA AIR LINES ";
char to[16] = "New York";
char from[16] = "Seattle";
unsigned int alt = 43219;
float dist = 20.05;

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

void displayPlane(){
  lcd.clear();
  lcd.setCursor(0,0);

  switch (state) {
    case 0:
      if (strlen(to) != 0 && strlen(from) != 0){
        lcd.print(from);
        lcd.write(byte(0)); //arrow
        lcd.print(to);
        break;
      }
    case 1: 
      if (strlen(model) != 0){
        lcd.print(model);
        break;
      }
    case 2:
      if (strlen(op) != 0){
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

