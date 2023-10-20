#include <SoftwareSerial.h> 

SoftwareSerial MyBlue(2, 3); // RX | TX 
void setup() 
{    
//  Serial.begin(9600);
  MyBlue.begin(9600);  
} 
void loop() 
{   
 if (MyBlue.available()) {
   String command = MyBlue.readString(); 
//   Serial.println(command);
   if(command == "Scan")
   {
        char Data[800];
        for(int i =0 ; i < 800 ; i++) Data[i] = ' ';
        int index = 0;
        for (int i = 0; i <= 180; i++) {
          // instead of 250 use ultrasonic sensor data
          String data = String(250)+" ";
          for(int j = 0 ; j < data.length() ;j++)
          {
            Data[index] = data[j];
            index++;
          }
        }
        Data[799] = '\0';
        MyBlue.print(Data);
//        Serial.println(Data);
   }
 } 
}
