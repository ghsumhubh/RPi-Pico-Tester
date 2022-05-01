import utime
from Machine import Pin


# Class private constants and definition 
# ----------------------------------------------------------------------------
class ST7036:
    CMD_DELAY           = 1;  # Command delay in miliseconds
    CHAR_DELAY          = 0;  # Delay between characters in miliseconds
    PIXEL_ROWS_PER_CHAR = 8;  # Number of pixel rows in the LCD character
    MAX_USER_CHARS      = 16; # Maximun number of user defined characters

    # LCD Command set
    DISP_CMD       = 0x0;  # Command for the display
    RAM_WRITE_CMD  = 0x40; # Write to display RAM
    CLEAR_DISP_CMD = 0x01; # Clear display command
    HOME_CMD       = 0x02; # Set cursos at home (0,0)
    DISP_ON_CMD    = 0x0C; # Display on command
    DISP_OFF_CMD   = 0x08; # Display off Command
    SET_DDRAM_CMD  = 0x80; # Set DDRAM address command
    CONTRAST_CMD   = 0x70; # Set contrast LCD command
    FUNC_SET_TBL0  = 0x38; # Function set - 8 bit, 2 line display 5x8, inst table 0
    FUNC_SET_TBL1  = 0x39; # Function set - 8 bit, 2 line display 5x8, inst table 1

    # LCD bitmap definition
    CURSOR_ON_BIT  = ( 1 << 1 );# Cursor selection bit in Display on cmd.
    BLINK_ON_BIT   = ( 1 << 0 );# Blink selection bit on Display on cmd. 

    # Driver DDRAM addressing
    dram_dispAddr = [
    [ 0x00, 0x00, 0x00 ],  # One line display address
    [ 0x00, 0x40, 0x00 ],  # Two line display address
    [ 0x00, 0x10, 0x20 ]   # Three line display address
    ]

    def __init__(self, num_lines, num_col, i2cAddr, r,g,b ):
        self.num_lines  = num_lines
        self.num_col      = num_col
        self.i2cAddress   = ( i2cAddr >> 1 )
        self.cmdDelay     = ST7036.CMD_DELAY
        self.charDelay    = ST7036.CHAR_DELAY
        self.initialised  = False
        self.r = r
        self.g = g
        self.b = b


    # Functions: modifiers (set), selectors (get) and class methods
    # ---------------------------------------------------------------------------
    def init ():
    size_t retVal; 
    Wire.beginTransmission ( _i2cAddress );
    Wire.write ( (byte)0x0 );   # Send command to the display
    Wire.write ( FUNC_SET_TBL0 );
    utime.sleep_ms(10)
    Wire.write ( FUNC_SET_TBL1 );
    utime.sleep_ms(10)
    Wire.write ( 0x14 );  # Set BIAS - 1/5
    Wire.write ( 0x73 );  # Set contrast low byte
    Wire.write ( 0x5E );  # ICON disp on, Booster on, Contrast high byte 
    Wire.write ( 0x6D );  # Follower circuit (internal), amp ratio (6)
    Wire.write ( 0x0C );  # Display on
    Wire.write ( 0x01 );  # Clear display
    Wire.write ( 0x06 );  # Entry mode set - increment
    _status = Wire.endTransmission ();
    
    if ( _status == 0 )
    {
        _initialised = true;
    }
    }


    void ST7036::setDelay (int cmdDelay,int charDelay) 
    {
        _cmdDelay = cmdDelay;
        _charDelay = charDelay;
    }


    void ST7036::command(uint8_t value) 
    {
    # If the LCD has been initialised correctly, write to it
    if ( _initialised )
    {
        Wire.beginTransmission ( _i2cAddress );
        Wire.write ( DISP_CMD );
        Wire.write ( value );
        _status = Wire.endTransmission ();
        delay(_cmdDelay);
    }
    }


    size_t ST7036::write(uint8_t value) 
    {
    # If the LCD has been initialised correctly write to it
    # -----------------------------------------------------
    if ( _initialised )
    {
        
        # If it is a new line, set the cursor to the next line (1,0)
        # ----------------------------------------------------------
        if ( value == '\n' )
        {
            setCursor (1,0);
        }
        else
        {
            Wire.beginTransmission ( _i2cAddress );
            Wire.write ( RAM_WRITE_CMD );
            Wire.write ( value );
            _status = Wire.endTransmission ();
            delay(_charDelay);
        }
    }
    }

    size_t ST7036::write(const uint8_t *buffer, size_t size)
    {
    # If the LCD has been initialised correctly, write to it
    # ------------------------------------------------------
    if ( _initialised )
    {
        Wire.beginTransmission ( _i2cAddress );
        Wire.write ( RAM_WRITE_CMD );
        Wire.write ( (uint8_t *)buffer, size );
        _status = Wire.endTransmission ();
        delay(_charDelay);
    }
    }


    void ST7036::clear()
    {
    command (CLEAR_DISP_CMD);
    }


    void ST7036::home()
    {
    command ( HOME_CMD );
    }


    void ST7036::on()
    {   
    command ( DISP_ON_CMD );
    }


    void ST7036::off()
    {
    command ( DISP_OFF_CMD );        
    }


    void ST7036::cursor_on()
    {
    command ( DISP_ON_CMD | CURSOR_ON_BIT );
    }

    void ST7036::cursor_off()
    {
    command ( DISP_ON_CMD & ~(CURSOR_ON_BIT) );
    }

    void ST7036::blink_on()
    {
    command ( DISP_ON_CMD | BLINK_ON_BIT );
    }

    void ST7036::blink_off()
    {
    command ( DISP_ON_CMD & ~(BLINK_ON_BIT) ); 
    }


    void ST7036::setCursor(uint8_t line_num, uint8_t x)
    {
    uint8_t base = 0x00;
    
    # If the LCD has been initialised correctly, write to it
    # ------------------------------------------------------
    if ( _initialised )
    {
        # set the baseline address with respect to the number of lines of
        # the display 
        base = dram_dispAddr[_num_lines-1][line_num];
        base = SET_DDRAM_CMD + base + x;
        command ( base );
    }
    }

    #ifdef _LCDEXPANDED
    uint8_t ST7036::status(){
        
        return _status;
    }


    uint8_t ST7036::keypad ()
    {
    # NOT SUPPORTED
    return 0;
    }


    void ST7036::load_custom_character (uint8_t char_num, uint8_t *rows)
    {
    # If the LCD has been initialised correctly start writing to it
    # --------------------------------------------------------------------------
    if ( _initialised )
    {
        # If it is a valid place holder for the character, write it into the
        # display's CGRAM
        # --------------------------------------------------------------------------
        if ( char_num < MAX_USER_CHARS )
        {
            # Set up the display to write into CGRAM - configure LCD to use func table 0
            Wire.beginTransmission ( _i2cAddress );
            Wire.write ( DISP_CMD );
            Wire.write ( FUNC_SET_TBL0 ); # Function set: 8 bit, 2 line display 5x8, funct tab 0
            delay ( _cmdDelay );
            
            # Set CGRAM position to write
            Wire.write ( RAM_WRITE_CMD + (PIXEL_ROWS_PER_CHAR * char_num) ); 
            _status = Wire.endTransmission ();
            
            # If we have changed the function table and configured the CGRAM position
            # write the new character to the LCD's CGRAM
            # -----------------------------------------------------------------------
            if ( _status == 0 )
            {
                write ( rows, PIXEL_ROWS_PER_CHAR ); # write the character to CGRAM 
                
                # Leave the LCD as it was - function table 1 DDRAM and set the cursor 
                # position to (0, 0) to start writing.
                command ( FUNC_SET_TBL1 );
                setCursor ( 0,0 );
            }
        }
    }
    }


    void ST7036::setBacklight(uint8_t new_val)
    {
    # Set analog write to the pin, the routine already checks if it can
    # set a PWM or not.
    # -----------------------------------------------------------------
        if ( _backlightPin != -1 )
    {
        analogWrite ( _backlightPin, new_val );
    }
    }


    void ST7036::setContrast(uint8_t new_val)
    {
    # Only allow 15 levels of contrast
        new_val = map ( new_val, 0, 255, 0, 15 );
    
    command(CONTRAST_CMD + new_val);
    }
