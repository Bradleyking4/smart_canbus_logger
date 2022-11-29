// demo: CAN-BUS Shield, receive data with check mode
// send data coming to fast, such as less than 10ms, you can use this way
// loovee, 2014-6-13

#include <SPI.h>

#include "mcp_can.h"

// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 10;

MCP_CAN CAN(SPI_CS_PIN);  // Set CS pin

const int supported_bit_rates[8] = {CAN_10KBPS, CAN_20KBPS, CAN_50KBPS, CAN_100KBPS, CAN_125KBPS, CAN_250KBPS, CAN_500KBPS, CAN_1000KBPS};

void setup() {
  Serial.begin(250000);
  byte incoming = 0;
  int baudConfig;
  while (true) {
    if (Serial.available() > 0) {
      incoming = Serial.read();
      Serial.write(incoming);
      if (incoming >= 0 && incoming < 8) {
        baudConfig = supported_bit_rates[incoming];
        Serial.write("Baud rate is set: ");
        Serial.println(baudConfig);
        break;
      } else {
        Serial.println("Unsupported baud rate!");
      }
    }
  }

  while (CAN_OK != CAN.begin(baudConfig, MCP_8MHz))  // init can bus : baudrate = 500k
  {
    Serial.println("CAN BUS Shield init fail");
    Serial.println(" Init CAN BUS Shield again");
    delay(100);
  }
  Serial.println("CAN BUS Shield init ok!");
}

inline void send_data(byte *data_out, uint32_t id_out) {
  Serial.write("~");
  for (int i = 0; i < 8; i++) {
    Serial.write(data_out[i]);
  }
  unsigned char *id = (unsigned char *)&id_out;
  for (int i = 3; i >= 0; i--) Serial.write(id[i]);

  Serial.write(".\n");
}

char inBuffer[20];
byte index = 0;

void loop() {
  unsigned char len = 0;
  unsigned char buf[8];

  if (CAN_MSGAVAIL == CAN.checkReceive())  // check if data coming
  {
    CAN.readMsgBuf(&len, buf);  // read data,  len: data length, buf: data buf

    unsigned long canId = CAN.getCanId();
    send_data(buf, canId);
  }

  if (Serial.available() > 0) {
    inBuffer[index] = Serial.read();
    if (inBuffer[index] == '\n') {
      if (inBuffer[0] == '~' && inBuffer[13] == '.') {
        int ID =  (inBuffer[9]<<24) + (inBuffer[10]<<16) + (inBuffer[11]<<8) + inBuffer[12];
        CAN.sendMsgBuf(ID, 0, 8, &inBuffer[1]);
      }
      inBuffer[0] = 0;
      inBuffer[12] = 0;
      index = 0;
    } else {
      if(inBuffer[0] == '~'){     
        index++;
      }
    }
  }
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
