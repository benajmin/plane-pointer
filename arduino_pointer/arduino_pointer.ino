/*  Plane Pointer
 *  Benjamin Wilkins
 *  December 3, 2017
 *  
 *  Requires LCD I2C library
 *  https://bitbucket.org/fmalpartida/new-liquidcrystal/downloads
 */

#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define YAW_SERVO_PIN 5
#define PITCH_SERVO_PIN 6

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

Servo yaw_servo;
Servo pitch_servo;

void setup() {
  yaw_servo.attach(YAW_SERVO_PIN);
  pitch_servo.attach(PITCH_SERVO_PIN);
  
  Serial.begin(9600);
  lcd.begin(16,2);

  lcd.backlight();

  lcd.setCursor(0,0); 
  lcd.print("Plane Pointer");
  lcd.setCursor(0,1);
  lcd.print("Benjamin Wilkins");
  delay(8000);  
}

void loop() {
  // put your main code here, to run repeatedly:

}
