
const long T = F_CPU / 9600;

void delay_1(){
for (int i = 0; i< T; i++){
  asm("NOP");
}
}


void setup() {
  // put your setup code here, to run once:
  pinMode(4, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned char mensagem = 'C';  
  
  digitalWrite(4, HIGH);
  delay(1000);
  digitalWrite(4, LOW);
  delay_1();

  for (int i = 0; i< 8; i++){
    digitalWrite(4, mensagem >> i & 0x01);
    delay_1();
  }
  

 

}
