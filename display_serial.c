/*
Hardware notes
===============================================================================

	PB1 and PB2 are now used for software serial!
	except PB1 is also used to drive LEDs
	so I'm justing using PB2 to recieve serial
	
	the internal RC oscillator runs at 8MHz but
	currently its clocked down to 1MHz since 8MHz was giving glitchy
	programming.
	
	common baud rates are
		2400,4800,9600,19200,38400,57600
	
	assuming we want to spend no more than 10% of our time handling interrupts
	and that we want to poll at 4x the baud rate to avoid aliasing problems.
	
	consider baud rate 2400
	we'd like to sample just slightly slower than twice this rate
	so a tad slower than 4800 Hz.
	our clock is 1MHz = 1000000 Hz
	we're using a clock prescale of 2 which means A prescaler of 8 on top
	of the clock for our interrupt timer thingy
	timer frequency = 125000 Hz
	so what interval in timer cycles should we poll? 
	125000 Hz / 4800 Hz ~= 26.0416666667
	Since we're trying to be a bit slow lets call this 27 cycles.
	
	update: doubled baud rate, change scan cycle to match
	

	DDRx   : 1 = output, 0 = input
	PORTx : output buffer
	PINx  : digital input buffer ( writes set pullups )
	Port B is the chip IO port ( other ports are control registers )

		AtTiny24 pinout:
		            __ __
		3     VCC -|  U  |- GND    1
		  BCK PB0 -|     |- PA0 G1
		  SHU PB1 -|     |- PA1 B1
		4 RST PB3 -|     |- PA2 R1
		  PLY PB2 -|     |- PA3 G2 
		  FWD PA7 -|     |- PA4 B2 5
		2 IND PA6 -|_____|- PA5 R2 6
		        
		Programmer pinout, 6 pin:
		        
		6 MISO +-+  VCC 3
		5 SCK  + + MOSI 2 
		4 RST  +-+  GND 1
		
		Programmer pinout, 10 pin:
		        
		3 vcc  +-+   MOSI 2
		       + +    
		       + +]  RST  4 
		       + +   SCK  5 
		1 gnd  +-+   MISO 6
		
	PORT : write to here to set output
	DDR  : write to here to set IO. 1 for output.
	PIN  : pull ups ? digital input ?

thanks to http://brownsofa.org/blog/archives/215 for explaining timer interrupts

=============================================================================*/

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#define NOP __asm__("nop\n\t")
#define N 10
#define SCANRATE 13

uint16_t b0[N+1],b1[N+1];
uint16_t *disp = &b0[0];
uint16_t *buff = &b1[0];
volatile uint8_t scanI = 0;

// gets pixel data from the marquee
uint8_t get(uint8_t r, uint8_t c, uint16_t *d)  { 
	if (c<4)	  c += 6;
	else if (c<9) c -= 4;
	else {
		c -= c<13? 3 : 13;
		r += 5;
	}
	if (r==c) c=5;
    return d[r]>>c&1;
}

// sets a pixel on the marquee
void set(uint8_t r, uint8_t c, uint8_t v, uint16_t *d)  { 
	if (c<4)	  c += 6;
	else if (c<9) c -= 4;
	else {
		c -= c<13? 3 : 13;
		r += 5;
	}
	if (r==c) c=5;
    if ((d[r]>>c&1)!=v) d[r]^=1<<c;
}

#define WAITING 0
#define STARTING 1
#define RECIEVING 2
volatile uint8_t state = WAITING;
volatile uint8_t current = 1;
volatile uint8_t ticks = 0; 
volatile uint8_t data = 0;
volatile uint8_t recieved = 0;
volatile uint8_t c = 0;
volatile uint8_t newdata = 0;
volatile uint8_t data_ready = 0;
ISR(TIM0_COMPA_vect) {
	int input = (PINB&0b00000100)>>2;
	//delay(5);
	if (state==WAITING) {
		if (input) return; //continue waiting
		// line has been pulled low -- signal imminent. 
		// we should have one or two cycles of this start signal
		// followed by eight bits of data signals
		// the signal may remain low for the entire duraion 
		state = STARTING;
		return;
	}
	if (state==STARTING) {
		//last time, we saw a low level, letting us know a signal is coming
		//now we should accept one or two low pulses 
		//er.. that is, zero or one more pulse
		//zero if and only if we seem to switch to 1 early
		//otherwise eat the one. 
		data = ticks = recieved = 0;
		state = RECIEVING;
		if (!input) return; //consume -- any more 0s will be treated as data
		// we got a 1 .. must have exited the init signal early, missed a beat
		// no matter, drop down into recieving code
	}
	if (state==RECIEVING) {
		if (ticks) {
			//ticks 1: either this is the second signal of the previous bit, 
			//or, if it differs, the first signal of the next bit
			//either way this will be the last of this bit
			data = (data<<1)|current;
			//set(0,recieved,current,disp);
			recieved++;
			if (recieved>=8) { 
				newdata = data;
				data_ready =1;
				state = WAITING;
				return; // this should be all we need, go into standby mode
			}
			if (input==current) {
				// its the same -- treat it like the second signal
				// prepare to recieve something else next time		
				ticks = 0;
				return;
			}
			// I guess we missed a step, well, this is the next signal
			// already, better handle it!
			// drop through to the first signal code below
		}
		// first signal of a new bit
		current = input;
		ticks = 1;
	}
}

int main() {	
	
	uint8_t i,j,shifting,incoming;

	// zero out the display data
	for (i=0; i<=N; i++) buff[i] = disp[i] = 1<<i;
	
	// Setup timer interrupts for software serial
	// See the Attiny24 datasheet for the meanings of these registers
	TIMSK0 = 2;        // Timer CompA interupt
	TCCR0B = 2;        // speed
	TCCR0A = 2;        // CTC mode
	OCR0A  = SCANRATE; // period
	sei();
	
	while (1) {
		// if our software serial code has data ready for us, it will
		// set the data_ready flag to 1, and we will consume that data
		// and start sending it to the screen
		if (data_ready) {
			shifting=1;
			incoming=newdata;
			data_ready=0;
			i=j=0;
		}
		
		// If we are shifting in a new column, we copy all the pixles to 
		// the left, then write in the new column. Since the display 
		// scanning happens below and is not interrupt driven,
		// We only do little bit of work on each pass through the loop --
		// otherwise the display would visible stall when we send new data
		if (shifting) {
			if (++j>=5) {
				j=0;
				if (++i>=17) {
					// shifting complete -- write in new data
					for (j=0;j<5;j++) 
						set(j,17,(data>>(7-j))&1,buff);
					// flip buffers to show new screen
					uint16_t *temp = buff; 
					buff = disp; 
					disp = temp;
					shifting=0;				
				}
			}
			if (shifting) set(j,i,get(j,i+1,disp),buff);
		}
		
		// SCAN DISPLAY
		uint16_t ddr = disp[scanI];
		uint16_t pin = ~(1<<scanI);
		pin &= ddr;
		if (scanI==N) pin=~pin;
		DDRA  = 0  ; DDRB  = 0;
		PORTA = pin; PORTB = pin>>8&0b11;
		DDRA  = ddr; DDRB  = ddr>>8&0b11;
		if (++scanI>N) scanI=0;
	}
} 





