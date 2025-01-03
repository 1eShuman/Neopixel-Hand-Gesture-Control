#include <Adafruit_NeoPixel.h>


#define neoPin 14
#define pixelsNum 8


Adafruit_NeoPixel pixels = Adafruit_NeoPixel(pixelsNum, neoPin, NEO_GRB + NEO_KHZ800);


void setup() {
  Serial.begin(9600);
  pixels.begin();
  pixels.clear();
}


void loop() {
  if (Serial.available() > 0) {
    int number = Serial.parseInt();
   
    switch (number){
      case 0:
        pixels.clear();
        pixels.show();
        break;
      case 1:
      pixels.clear();
      pixels.setPixelColor(0, 125, 0, 0);
      pixels.show();
      break;
      case 2:
      pixels.clear();
      pixels.setPixelColor(0, 125, 0, 0);
      pixels.setPixelColor(1, 125, 70, 0);
      pixels.show();
      break;
      case 3:
      pixels.clear();
      pixels.setPixelColor(0, 125, 0, 0);
      pixels.setPixelColor(1, 125, 70, 0);
      pixels.setPixelColor(2, 70, 125, 0);
      pixels.setPixelColor(3, 0, 125, 0);
      pixels.show();
      break;
      case 4:
      pixels.clear();
      pixels.setPixelColor(0, 125, 0, 0);
      pixels.setPixelColor(1, 125, 70, 0);
      pixels.setPixelColor(2, 70, 125, 0);
      pixels.setPixelColor(3, 0, 125, 0);
      pixels.setPixelColor(4, 0, 70, 125);
      pixels.setPixelColor(5, 0, 0, 125);
      pixels.show();
      break;
      case 5:
      pixels.clear();
      pixels.setPixelColor(0, 125, 0, 0);
      pixels.setPixelColor(1, 125, 70, 0);
      pixels.setPixelColor(2, 70, 125, 0);
      pixels.setPixelColor(3, 0, 125, 0);
      pixels.setPixelColor(4, 0, 70, 125);
      pixels.setPixelColor(5, 0, 0, 125);
      pixels.setPixelColor(6 ,70, 0, 125);
      pixels.setPixelColor(7 ,125, 0, 125);
      pixels.show();
      break;
    }


  }
}



