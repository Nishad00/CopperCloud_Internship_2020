/*
  Arduino Wireless Network - Multiple NRF24L01 Tutorial
 == Example 01 - Servo Control / Node 00 - Potentiometer ==
*/
#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>
RF24 radio(10, 9);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 00;   // Address of this node in Octal format ( 04,031, etc)
const uint16_t node01 = 01;      
void setup() {
  SPI.begin();
  radio.begin();
  network.begin(90, this_node);  //(channel, node address)
}
void loop() {
  network.update();
  unsigned long potValue = analogRead(A0);  // Read the potentiometer value
  unsigned long angleValue = map(potValue, 0, 1023, 0, 180); // Convert the value to 0-180
  RF24NetworkHeader header(node01);     // (Address where the data is going)
  bool ok = network.write(header, &angleValue, sizeof(angleValue)); // Send the data
}
