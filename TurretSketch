#include <Servo.h>

Servo servoH;  // horizontal (pan)
Servo servoV;  // vertical (tilt)

const int SERVO_H_PIN = 9;
const int SERVO_V_PIN = 8;

// Start centered
int posH = 90;
int posV = 115;

// Tuning
const int DEADBAND = 1;     
const float KP = 0.082;       
const int STEP_LIMIT = 50;    
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

// Serial line buffer
String line;

void setup() {
  servoH.attach(SERVO_H_PIN);
  servoV.attach(SERVO_V_PIN);
  servoH.write(posH);
  servoV.write(posV);

  Serial.begin(115200);
  delay(500);
}

void loop() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      processLine(line);
      line = "";
    } else {
      line += c;
    }
  }
}

void processLine(const String& s) {
  long cx = 0, cy = 0, dx = 0, dy = 0;
  if (!extractLong(s, "CX:", cx)) return;
  if (!extractLong(s, "CY:", cy)) return;
  if (!extractLong(s, "DX:", dx)) return;
  if (!extractLong(s, "DY:", dy)) return;

  if (abs(dx) < DEADBAND) dx = 0;
  if (abs(dy) < DEADBAND) dy = 0;

  posH = round(-dx * KP+90);
  posV = round(-dy*KP+115);

  servoH.write(posH);
  servoV.write(posV);
}

// Helpers
bool extractLong(const String& s, const char* key, long& out) {
  int k = s.indexOf(key);
  if (k < 0) return false;
  k += strlen(key);
  int end = s.indexOf(',', k);
  if (end < 0) end = s.length();
  String num = s.substring(k, end);
  num.trim();
  if (num.length() == 0) return false;
  out = num.toInt();  // tolerates leading +/-
  return true;
}
