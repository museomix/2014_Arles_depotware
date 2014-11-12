#define OUTPUT_LED  13
//#define OBJ1 3
const int objectPins[] = { 2, 3, 4, 5, 6 };
const int nbObj = 5;
const long delayTime = 500;
int misssingObject[] = { 1, 1, 1, 1, 1 };
boolean absenceDetected = false;
String serialized = "";
String lastSerialized = "00000";

void setup() {
      //pinMode(OBJ1, INPUT_PULLUP);
      // use a for loop to initialize each pin as an input in pullup mode:
      for (int i = 0; i < nbObj; i++)  {
        pinMode(objectPins[i], INPUT_PULLUP);      
      }
      pinMode(OUTPUT_LED,  OUTPUT);
      // Init liason série.
      Serial.begin(9600);
}

void loop() {
 //int absence1 = !digitalRead(OBJ1);
 // lecture des pins
 absenceDetected = false;
 for (int i = 0; i < nbObj; i++)  {
   misssingObject[i] = !digitalRead(objectPins[i]); 
   if ( misssingObject[i] && !absenceDetected) {
     absenceDetected = true;
   }
 }

 // Sending values to computer
 serialized = "";
 for (int i = 0; i < nbObj; i++)  {
   serialized += misssingObject[i];      
 }
 
 // N'envoyer les donnée que si elles ont changé.
 if (lastSerialized != serialized) {
   Serial.println(serialized);
   lastSerialized = serialized;
 }
 
 if (absenceDetected) {
   digitalWrite(OUTPUT_LED, HIGH);
 } else {
   digitalWrite(OUTPUT_LED, LOW);
 }
 // delay in between reads for stability
 delay(delayTime); 
}

