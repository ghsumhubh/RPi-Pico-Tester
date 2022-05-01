from machine import Pin
from time import sleep

text1 = "NEWHAVEN DisplayXXXX"
text2= "2x20 LCD Module XXXX"
SDA = Pin(26, Pin.OUT)					
SCL = Pin(27, Pin.OUT)						
#*****************************************************#
Slave = 0x78
Comsend = 0x00
Datasend = 0x40
Line2 = 0xC0
#*****************************************************#
def delay(n):				
    sleep(2)
#*****************************************************#
def I2C_out(j):
    d = j
    for n in range(0, 8):
        if (d & 0x80)==0x80:
            SDA.value(1)
        else:
            SDA.value(0)
        d = (d << 1)
        SCL.value(0)
        SCL.value(1)
        SCL.value(0)
    SCL.value(1)
    while 

	for(n=0n<8n++){
		if((d&0x80)==0x80)
		SDA=1
		else
		SDA=0
		d=(d<<1)
		SCL = 0
		SCL = 1
		SCL = 0
		}
	SCL = 1
	while(SDA==1){
		SCL=0
		SCL=1
		}
	SCL=0
}
#*****************************************************#
void I2C_Start(void)
{
	SCL=1
	SDA=1
	SDA=0
	SCL=0
}
#*****************************************************#
void I2C_Stop(void)
{
	SDA=0
	SCL=0
	SCL=1
	SDA=1
}
#*****************************************************#
void Show(unsigned char *text)
{
	int n,d
	d=0x00
	I2C_Start()
	I2C_out(Slave)
	I2C_out(Datasend)
	for(n=0n<20n++){
		I2C_out(*text)
		++text
		}
	I2C_Stop()
}
#*****************************************************#
void nextline(void)
{
	I2C_Start()
	I2C_out(Slave)
	I2C_out(Comsend)
	I2C_out(Line2)
	I2C_Stop()
}
#****************************************************
*           Initialization For ST7036i              *
*****************************************************#
void init_LCD() 
{
I2C_Start()
I2C_out(Slave)
I2C_out(Comsend)
I2C_out(0x38)
delay(10)
I2C_out(0x39)
delay(10)
I2C_out(0x14)
I2C_out(0x78)
I2C_out(0x5E)
I2C_out(0x6D)
I2C_out(0x0C)
I2C_out(0x01)
I2C_out(0x06)
delay(10)
I2C_Stop()
}
#*****************************************************#
#*****************************************************#
int main(void)
{
int i
P1 = 0
P3 = 0
while(1) 								#continue 
{
	init_LCD()
	delay(2)
	
	Show(text1)
	nextline()
	Show(text2)
	delay(2000)
	
	init_LCD()
	delay(2)
	
	I2C_out(Slave)
	I2C_out(Datasend)
	for(i=0i<20i++){#show first 20 chars in font table
	  I2C_out(i)}
	I2C_Stop()
	delay(4000)
}
}
