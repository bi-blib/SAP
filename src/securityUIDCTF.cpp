/*
 * --------------------------------------------------------------------------------------------------------------------
 * Security program
 * --------------------------------------------------------------------------------------------------------------------
 * This is adapted from MFRC522 library; for further details and other examples see: https://github.com/miguelbalboa/rfid
 */

#include <SPI.h>
#include <MFRC522.h>

#define GREEN 6
#define BLUE 4
#define RED 2
#define SS_PIN 10
#define RST_PIN 9
 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

// Init array that will store new NUID 
byte nuidPICC[4];

byte targetUID[] = {0xA3, 0x25, 0x15, 0x2A};  // Target UID in hexadecimal
byte uidSize = 4; 
byte uID_array[10];

void setup() { 
  Serial.begin(9600);

  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(RED, OUTPUT);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println(F("This code scan the MIFARE Classsic UID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}
 
void loop() {

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  Serial.println();
  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
      digitalWrite(BLUE, HIGH);
      Serial.println(F("Your tag is not of type MIFARE Classic."));
      delay(5000);
      digitalWrite(BLUE, LOW);
    
    return;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] || 
    rfid.uid.uidByte[1] != nuidPICC[1] || 
    rfid.uid.uidByte[2] != nuidPICC[2] || 
    rfid.uid.uidByte[3] != nuidPICC[3] ) {
    Serial.println(F("A new card has been detected."));

    // Store NUID into nuidPICC array
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
   
    Serial.println(F("The UID tag is:"));
    Serial.print(F("In hex: "));
    printHex(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
  }
  else Serial.println(F("Card read previously."));

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
}


/**
 * Helper routine to dump a byte array as hex values to Serial. 
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    uID_array[i] = buffer[i]; 
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
  bool uidMatch = true; 

  for (byte i = 0; i < uidSize; i++) {
      if (uID_array[i] != targetUID[i]) {
          uidMatch = false;
          break; 
      }
  }
  if (uidMatch) {
    Serial.println();
    Serial.print("WOAH your UID matches the my UID! I guess UIDs aren't secure :(");
    Serial.println();
    Serial.print("Flag is COMP6841{SEE_UID_IS_SO_EASY!}");
    digitalWrite(GREEN, HIGH);
    delay(5000);
    digitalWrite(GREEN, LOW);
  } else {
      Serial.println();
      Serial.print("HAHA you can never beat me! UID does not match.");
      Serial.println();
      digitalWrite(RED, HIGH);
      delay(5000);
      digitalWrite(RED, LOW);
  }
}