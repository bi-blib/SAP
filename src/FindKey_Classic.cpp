#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>


#define RST_PIN 9
#define SS_PIN 10
#define MIFARE_BLOCK_SIZE 16 // Define the size of MIFARE block

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

// Define MIFARE_Key structure as required by the MFRC522 library
MFRC522::MIFARE_Key defaultKeys[] = {
    {{0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}}, // Key 0
    {{0xA0, 0xA0, 0xA0, 0xA0, 0xA0, 0xA0}}, // Key 1
    {{0xB0, 0xB0, 0xB0, 0xB0, 0xB0, 0xB0}}  // Key 2
};

void setup() {
    Serial.begin(9600);
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("Scan a Card...");
}
void loop() {
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        delay(50);
        return;
    }

    Serial.print("Card UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        Serial.print(mfrc522.uid.uidByte[i], HEX);
        Serial.print(" ");
    }
    Serial.println();

    byte block = 0; // Specify the block you want to authenticate and read
    
    for (byte i = 0; i < 256; i++) {
        MFRC522::MIFARE_Key testKey;
        for (byte j = 0; j < MFRC522::MF_KEY_SIZE; j++) {
            testKey.keyByte[j] = i; // This creates keys like 00, 01, ..., 0F, 10, ..., FF
        }

        // Attempt to authenticate
        if (mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &testKey, &(mfrc522.uid)) == MFRC522::STATUS_OK) {
            Serial.println("Authentication success for KeyA with Key:");
            for (byte k = 0; k < 6; k++) {
                Serial.print(testKey.keyByte[k], HEX);
                Serial.print(" ");
            }
            Serial.println();

            byte buffer[MIFARE_BLOCK_SIZE];
            byte size;

            // Read data from the specified block
            if (mfrc522.MIFARE_Read(block, buffer, &size) == MFRC522::STATUS_OK) {
                Serial.print("Block data: ");
                for (byte k = 0; k < MIFARE_BLOCK_SIZE; k++) {
                    Serial.print(buffer[k], HEX);
                    Serial.print(" ");
                }
                Serial.println();
            } else {
                Serial.println("Failed to read block.");
            }
            break; // Exit loop on success
        } else {
            Serial.println("Authentication failed with this key.");
        }
      delay(50);
    }

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
} 