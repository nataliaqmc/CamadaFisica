#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 5, 1, 8, SW_UART_EVEN_PARITY);
  digitalWrite(5, HIGH);
}

void loop() {
 send_byte();
 delay(2000);
}



void send_byte() {
  char data = 'a';
  sw_uart_write_byte(&uart, data);
}
