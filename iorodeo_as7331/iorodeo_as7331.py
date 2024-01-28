import time
from adafruit_bus_device.i2c_device import I2CDevice

DEFAULT_I2C_ADDR = const(0x74)

# Control/Configuration register bank
_REG_ADDR_OSR    = const(0x00) # Operational State Register
_REG_ADDR_AGEN   = const(0x02) # API Generation Register
_REG_ADDR_CREG1  = const(0x06) # Configuration Register 1
_REG_ADDR_CREG2  = const(0x07) # Configuration Register 2
_REG_ADDR_CREG3  = const(0x08) # Configuration Register 3
_REG_ADDR_BREAK  = const(0x09) # Break Register
_REG_ADDR_EDGES  = const(0x0A) # Edges Register (for SYND mode)
_REG_ADDR_OPTREG = const(0x0B) # Option Register

# Output register bank (Measurement State) 
_REG_ADDR_STATUS   = const(0x00) # Status register 
_REG_ADDR_TEMP     = const(0x01) # Temperature measurement result
_REG_ADDR_MRES1    = const(0x02) # Channel A measurement result
_REG_ADDR_MRES2    = const(0x03) # Channel B measurement result
_REG_ADDR_MRES3    = const(0x04) # Channel C measurement result
_REG_ADDR_OUTCONVL = const(0x05) # Result of time conversion (lsb) 
_REG_ADDR_OUTCONVH = const(0x06) # Result of time conversion (msb)

# OSR REG Masks (RW)
_OSR_MASK_DOS      = const(0x07) # Device Operating State 
_OSR_MASK_SW_RES   = const(0x08) # Software Reset 
_OSR_MASK_PD       = const(0x40) # Power Down State Switch 
_OSR_MASK_SS       = const(0x80) # Start/Stop measurement  

# CREG1 Masks (RW)
_CREG1_MASK_INTEGRATION_TIME = const(0x0f) # Integration time
_CREG1_MASK_GAIN             = const(0xf0) # Irradiance reponsivity

# CREG2 Masks (RW)
_CREG2_MASK_EN_TM  = const(0x40) # Disable/enable measurement of integration time
_CREG2_MASK_EN_DIV = const(0x08) # Disable/enable divider of measurement results
_CREG2_MASK_DIV    = const(0x07) # Digital divider of measurement results

# CREG2 Masks (RW)
_CREG3_MASK_MMODE = const(0xc0) # Measurement mode
_CREG3_MASK_SB    = const(0x10) # Standby disable/enable
_CREG3_MASK_RDYOD = const(0x08) # Pin Ready push-pull or open-drain
_CREG3_MASK_CCLK  = const(0x03) # Internal clock frequency

# Status REG Masks (RO)
_STATUS_MASK_POWERSTATE   = const(0x01) # Power state  
_STATUS_MASK_STANDBYSTATE = const(0x02) # Standby state 
_STATUS_MASK_NOTREADY     = const(0x04) # Not ready state
_STATUS_MASK_NDATA        = const(0x08) # New measurements transferred
_STATUS_MASK_LDATA        = const(0x10) # Measurements overwritten
_STATUS_MASK_ADCOF        = const(0x20) # Overflow of internal conversion channel
_STATUS_MASK_MRESOF       = const(0x40) # Overflow of measurement result
_STATUS_MASK_OUTCONVOF    = const(0x80) # Overflow of time reference

# AGEN Register Masks
_AGEN_MASK_DEVID  = const(0xf0) # Device Id number
_AGEN_MASK_MUT    = const(0x0f) # Mutation number of control bank
_AGEN_SHIFT_DEVID = const(0x4)  # Shift value for dev id

# Device modes
DEVICE_STATE_CONFIGURATION = const(0x2)
DEVICE_STATE_MEASUREMENT   = const(0x3)
ALLOWED_DEVICE_STATES = (
        DEVICE_STATE_CONFIGURATION, 
        DEVICE_STATE_MEASUREMENT,
        )

# Mode to/from string conversions
DEVICE_STATE_TO_STRING = {
        DEVICE_STATE_CONFIGURATION : 'configuration', 
        DEVICE_STATE_MEASUREMENT   : 'measurement', 
        }
DEVICE_STATE_FROM_STRING = {v:k for k,v in DEVICE_STATE_TO_STRING.items()}

# Integration times (bits 3:0 of CREG1)
INTEGRATION_TIME_1MS     = const(0x00)
INTEGRATION_TIME_2MS     = const(0x01)
INTEGRATION_TIME_4MS     = const(0x02)
INTEGRATION_TIME_8MS     = const(0x03)
INTEGRATION_TIME_16MS    = const(0x04)
INTEGRATION_TIME_32MS    = const(0x05)
INTEGRATION_TIME_64MS    = const(0x06)
INTEGRATION_TIME_128MS   = const(0x07)
INTEGRATION_TIME_256MS   = const(0x08)
INTEGRATION_TIME_512MS   = const(0x09)
INTEGRATION_TIME_1024MS  = const(0x0a)
INTEGRATION_TIME_2048MS  = const(0x0b)
INTEGRATION_TIME_4096MS  = const(0x0c)
INTEGRATION_TIME_8192MS  = const(0x0d)
INTEGRATION_TIME_16384MS = const(0x0e)

_INTEGRATION_TIME_MIN_VAL = INTEGRATION_TIME_1MS
_INTEGRATION_TIME_MAX_VAL = INTEGRATION_TIME_16384MS 

# Gain settings (bits 7:4 CREG1)
GAIN_2048X = const(0x00)
GAIN_1024X = const(0x01)
GAIN_512X  = const(0x02)
GAIN_256X  = const(0x03)
GAIN_128X  = const(0x04)
GAIN_64X   = const(0x05)
GAIN_32X   = const(0x06)
GAIN_16X   = const(0x07)
GAIN_8X    = const(0x08)
GAIN_4X    = const(0x09)
GAIN_2X    = const(0x0a)
GAIN_1X    = const(0x0b)

_GAIN_MIN_VAL = const(0x00)
_GAIN_MAX_VAL = const(0x0b)
_GAIN_BIT_SHIFT = const(4)

# Measurement mode settings (bits 7:6 of CREG3) 
MEASUREMENT_MODE_CONTINUOUS         = const(0x00)
MEASUREMENT_MODE_COMMAND            = const(0x40)
MEASUREMENT_MODE_SYNC_START         = const(0x80) 
MEASUREMENT_MODE_SYNC_START_AND_END = const(0xc0)

ALLOWED_MEASUREMENT_MODES = (
        MEASUREMENT_MODE_CONTINUOUS,
        MEASUREMENT_MODE_COMMAND,
        MEASUREMENT_MODE_SYNC_START,
        MEASUREMENT_MODE_SYNC_START_AND_END,
        )

MEASUREMENT_MODE_TO_STRING = {
        MEASUREMENT_MODE_CONTINUOUS          : 'continuous',        
        MEASUREMENT_MODE_COMMAND             : 'command',           
        MEASUREMENT_MODE_SYNC_START          : 'sync_start',        
        MEASUREMENT_MODE_SYNC_START_AND_END  : 'sync_start_and_end',
        }

STRING_TO_MEASUREMENT_MODE = {v:k for k,v in MEASUREMENT_MODE_TO_STRING.items()}

# Internal clock frequencys
CCLK_FREQ_1024KHZ = const(0x00)
CCLK_FREQ_2048KHZ = const(0x01)
CCLK_FREQ_4096KHZ = const(0x02)
CCLK_FREQ_8192KHZ = const(0x03)

_CCLK_MIN_VAL = CCLK_FREQ_1024KHZ
_CCKL_MAX_VAL = CCLK_FREQ_8192KHZ

# Measurement divider min/max value
_DIV_MIN_VAL = const(0x00)
_DIV_MAX_VAL = const(0x07)

# Fullscale range values for UV A,B and C channels
_FSRA = const(348160)
_FSRB = const(387072)
_FSRC = const(169984)

class AS7331:

    """
    AS7331 Spectral UV sensor.  Implements I2C interface with the AS7331 
    sensor. 
    """

    def __init__(self, i2c_bus, address=DEFAULT_I2C_ADDR):
        self.i2c_device = I2CDevice(i2c_bus, address)

        # Keep local copies of gain, integration_time, etc the  for conversion
        # calculations that way we don't have request these each time we want
        # to convert a measurement. 
        self.software_reset()
        self.state_copy = {
                'gain'             : self.gain, 
                'integration_time' : self.integration_time, 
                'divider'          : self.divider, 
                'divider_enabled'  : self.divider_enabled,
                'measurement_mode' : self.measurement_mode,
                'cclk'             : self.cclk,
                }
        self.set_default_config()
        self.overflow_exception = False 

    def set_default_config(self):
        """
        Set the device configuration to default values
        """
        self.measurement_mode = MEASUREMENT_MODE_COMMAND
        self.integration_time = INTEGRATION_TIME_256MS
        self.gain = GAIN_16X
        self.standby_state = False
        self.power_down_enable = False 
        self.divider_enabled = False

        # TO DO
        # ------------------------------------------------------------------
        # Not complete, need to set a few more things such as divider, etc.
        # ------------------------------------------------------------------

        self.device_state = DEVICE_STATE_MEASUREMENT

    def read_uint16(self, reg):
        """ Reads two bytes (uint16) from the specified register """
        obuffer = bytearray(1)
        ibuffer = bytearray(2)
        obuffer[0] = reg
        with self.i2c_device as i2c:
            i2c.write_then_readinto(obuffer, ibuffer, out_end=1, in_end=2)
        lo_byte = ibuffer[0]
        hi_byte = ibuffer[1]
        return lo_byte, hi_byte

    def write_uint16(self, reg, lo_byte, hi_byte): 
        """ Writes two bytes (uint16) to the specified register """
        obuffer = bytearray(3)
        obuffer[0] = reg
        obuffer[1] = lo_byte
        obuffer[2] = hi_byte 
        with self.i2c_device as i2c:
            i2c.write(obuffer)

    def read_uint8(self, reg):
        """ Reads one byte (uint8) from the specified register """
        obuffer = bytearray(1)
        ibuffer = bytearray(1)
        obuffer[0] = reg
        with self.i2c_device as i2c:
            i2c.write_then_readinto(obuffer, ibuffer, out_end=1, in_end=1)
        return ibuffer[0]

    def write_uint8(self, reg, val):
        """ Writes one byte (uint8) to the specified register """
        obuffer = bytearray(2)
        obuffer[0] = reg
        obuffer[1] = val
        with self.i2c_device as i2c:
            i2c.write(obuffer)

    @property
    def osr(self):
        """ Reads the contents of the Operational State Register (OSR) """
        return self.read_uint8(_REG_ADDR_OSR)

    @osr.setter
    def osr(self, val):
        """ Writes to the Operational State Register (OSR) """
        self.write_uint8(_REG_ADDR_OSR, val)

    @property
    def osr_and_status(self):
        """ Reads both the Operational State Register (OSR) and Status Register. """
        byte0, byte1 = self.read_uint16(_REG_ADDR_STATUS)
        return byte0, byte1

    @property
    def status(self):
        """ Reads the Status Register """
        byte0, byte1 = self.read_uint16(_REG_ADDR_STATUS)
        return byte1
    @property
    def status_as_dict(self):
        """ Returns the contents of the status register as a dictionary """
        status_byte = self.status
        status_dict = { 
                'powerstate'   : bool(_STATUS_MASK_POWERSTATE   & status_byte), 
                'standbystate' : bool(_STATUS_MASK_STANDBYSTATE & status_byte),
                'notready'     : bool(_STATUS_MASK_NOTREADY     & status_byte),
                'ndata'        : bool(_STATUS_MASK_NDATA        & status_byte),
                'ldata'        : bool(_STATUS_MASK_LDATA        & status_byte),
                'adcof'        : bool(_STATUS_MASK_ADCOF        & status_byte),
                'mresof'       : bool(_STATUS_MASK_MRESOF       & status_byte),
                'outconvof'    : bool(_STATUS_MASK_OUTCONVOF    & status_byte),
                }
        return status_dict

    @property
    def notready(self):
        status_byte = self.status
        return bool(_STATUS_MASK_NOTREADY & status_byte)

    @property
    def creg1(self):
        """ Reads the contents of the CREG1 configuration register """
        return self.read_uint8(_REG_ADDR_CREG1)

    @creg1.setter
    def creg1(self, val):
        """ Writes to the CREG1 configuration register """
        self.write_uint8(_REG_ADDR_CREG1, val)

    @property
    def creg2(self):
        """ Reads the contents of the CREG2 configuration register """
        return self.read_uint8(_REG_ADDR_CREG2)

    @creg2.setter
    def creg2(self, val):
        """ Writes to the CREG2 configuration register """
        self.write_uint8(_REG_ADDR_CREG2, val)

    @property
    def creg3(self):
        """ Reads the contents of the CREG3 configuration register """
        return self.read_uint8(_REG_ADDR_CREG3)

    @creg3.setter
    def creg3(self, val):
        """ Writes to the CREG3 configuratino register """
        self.write_uint8(_REG_ADDR_CREG3, val)

    @property
    def temp(self):
        """ 
        Reads the TEMP register containing the temperature measurement. 
        The result is returned as raw bytes.   
        """
        lo_byte, hi_byte = self.read_uint16(_REG_ADDR_TEMP)
        return lo_byte, hi_byte

    @property
    def temp_as_uint16(self):
        return bytes_to_uint16(*self.temp)

    @property
    def mres1(self):
        """ 
        Reads the MRES1 regisister containing the measurement result of the 
        UVA channel. The result is returned as raw bytes.
        """
        lo_byte, hi_byte = self.read_uint16(_REG_ADDR_MRES1)
        return lo_byte, hi_byte

    @property
    def mres1_as_uint16(self):
        return bytes_to_uint16(*self.mres1)

    @property
    def mres2(self):
        """ 
        Reads the MRES2 register containing the measurement result of the
        UVB channel. The results is returned as raw bytes.  
        """
        lo_byte, hi_byte = self.read_uint16(_REG_ADDR_MRES2)
        return lo_byte, hi_byte

    @property
    def mres2_as_uint16(self):
        return bytes_to_uint16(*self.mres2)

    @property
    def mres3(self):
        """
        Reads the MRES1 regisister containing the measurement result of the 
        UVC channel. The result is returned as raw bytes.
        """
        lo_byte, hi_byte = self.read_uint16(_REG_ADDR_MRES3)
        return lo_byte, hi_byte

    @property
    def mres3_as_uint16(self):
        return bytes_to_uint16(*self.mres3)

    @property
    def power_down_enabled(self):
        """ Reads the power down state of the device True/False via the OSR """
        with ConfigurationStateManager(self):
            val = bool(self.osr & _OSR_MASK_PD)
        return val

    @power_down_enabled.setter
    def power_down_enabled(self,val):
        """ Sets the power down state of the device True/False via the OSR """
        with ConfigurationStateManager(self):
            if val:
                self.osr = self.osr | _OSR_MASK_PD
            else:
                self.osr = self.osr & ~_OSR_MASK_PD

    def software_reset(self):
        self.osr = self.osr | _OSR_MASK_SW_RES

    @property
    def device_state(self):
        """ 
        Reads the current device state from the Operational State Register (OSR).  

        Returns either DEVICE_STATE_CONFIGURATION or DEVICE_STATE_MEASUREMENT. 
        """
        return self.osr & _OSR_MASK_DOS

    @device_state.setter
    def device_state(self, new_mode):
        """ 
        Sets the current device state in the Operational State Register (OSR) 

        Can be set to either DEVICE_STATE_CONFIGURATION or DEVICE_STATE_MEASUREMENT.
        """
        if not new_mode in ALLOWED_DEVICE_STATES: 
            raise ValueError(f'unknown mode {new_mode}')
        self.osr = (self.osr & ~_OSR_MASK_DOS) | new_mode

    @property
    def device_state_as_string(self):
        """ 
        Gets the device state from the Operatinoal State Register (OSR) as a string. 

        Returns either 'measurement' or 'configuration'.

        """
        return DEVICE_STATE_TO_STRING.get(self.device_state, 'unknown')

    def device_state_from_string(self, mode_string):
        """ 
        Sets the device state in the Operation State Register from a string input. 

        Can be set to either 'measurement' or 'configuration'.
        """
        try:
            mode = DEVICE_STATE_FROM_STRING[mode_string]
        except KeyError:
            pass
        else:
            self.device_state = mode

    def start_measurement(self):
        """ Starts a one-shot measurement.  Used for measuremnts in command mode. """
        self.osr = self.osr | _OSR_MASK_SS

    @property
    def gain(self):
        """ 
        Gets the current gain setting from the CREG1 configuration register.

        Returns one of the following values: GAIN_2048X, GAIN_1024X, GAIN_512X,
        GAIN_256X, GAIN_128X, GAIN_64X, GAIN_32X, GAIN_16X, GAIN_8X, GAIN_4X,
        GAIN_2X, GAIN_1X.
        """
        with ConfigurationStateManager(self):
            val = (self.creg1 & _CREG1_MASK_GAIN) >> _GAIN_BIT_SHIFT
        return val

    @property
    def gain_value(self):
        """
        Returns gain as a numeric value
        """
        return gain_to_value(self.gain)

    @property
    def gain_as_string(self):
        """
        Gets the current gain values from the CREG1 configuration register as a
        string. 

        Returns one of the following values: '2048x', '1024x', '512x', '256x',
        '128x', '64x', '32x', '16x', '8x ', '4x', '2x', '1x' 
        """
        return f'{self.gain_value}x' 

    @gain.setter
    def gain(self, new_gain):
        """
        Sets the current gains value in the CREG1 configuration register. 

        Can be set to one of the following values: '2048x', '1024x', '512x',
        '256x', '128x', '64x', '32x', '16x', '8x ', '4x', '2x', '1x' 
        """

        with ConfigurationStateManager(self):
            if new_gain < _GAIN_MIN_VAL or new_gain > _GAIN_MAX_VAL:
                raise ValueError(f'unknown gain {new_gain}')
            self.creg1 = (self.creg1 & ~_CREG1_MASK_GAIN) | (new_gain << _GAIN_BIT_SHIFT)
            self.state_copy['gain'] = new_gain  

    @property
    def integration_time(self):
        """
        Gets the current integration time setting from the CREG1 configuration
        register. 

        Returns one of the following values: 
            INTEGRATION_TIME_1MS,
            INTEGRATION_TIME_2MS,
            INTEGRATION_TIME_4MS,
            INTEGRATION_TIME_8MS,
            INTEGRATION_TIME_16MS,
            INTEGRATION_TIME_32MS,
            INTEGRATION_TIME_64MS,
            INTEGRATION_TIME_128MS,
            INTEGRATION_TIME_256MS,
            INTEGRATION_TIME_512MS,
            INTEGRATION_TIME_1024MS,
            INTEGRATION_TIME_2048MS,
            INTEGRATION_TIME_4096MS,
            INTEGRATION_TIME_8192MS,
            INTEGRATION_TIME_16384MS,
        """
        with ConfigurationStateManager(self):
            val = self.creg1 & _CREG1_MASK_INTEGRATION_TIME
        return val

    @property
    def integration_time_value(self):
        """
        Gets the integration time as a numerical value (ms).
        """
        return integration_time_to_value(self.integration_time)

    @property
    def integration_time_as_string(self):
        """
        Gets the current integration time setting from the CREG1 configuration
        register as a string.

        Returns one of the following values: '1ms', '2ms', '4ms', '8ms',
        '16ms', '32ms', '64ms', '128ms', '256ms', '512ms', '1024ms', '2048ms',
        '4096ms', '8192ms', '16384ms',
        """
        return f'{self.integration_time_value}ms' 

    @integration_time.setter
    def integration_time(self, new_time):
        """
        Sets the integration time  via the CREG1 configuration register. 

        Can be set to one of the following values. 
            INTEGRATION_TIME_1MS,
            INTEGRATION_TIME_2MS,
            INTEGRATION_TIME_4MS,
            INTEGRATION_TIME_8MS,
            INTEGRATION_TIME_16MS,
            INTEGRATION_TIME_32MS,
            INTEGRATION_TIME_64MS,
            INTEGRATION_TIME_128MS,
            INTEGRATION_TIME_256MS,
            INTEGRATION_TIME_512MS,
            INTEGRATION_TIME_1024MS,
            INTEGRATION_TIME_2048MS,
            INTEGRATION_TIME_4096MS,
            INTEGRATION_TIME_8192MS,
            INTEGRATION_TIME_16384MS,
        """
        with ConfigurationStateManager(self):
            if new_time < _INTEGRATION_TIME_MIN_VAL or new_time > _INTEGRATION_TIME_MAX_VAL:
                raise ValueError(f'unknown integration time {new_time}')
            self.creg1 = (self.creg1 & ~_CREG1_MASK_INTEGRATION_TIME) | new_time
            self.state_copy['integration_time'] = new_time 

    @property
    def time_measurement_enabled(self):
        """
        Reads CREG2 and returns the time measurement enabled setting (True/False)
        """
        with ConfigurationStateManager(self):
            val = bool(self.creg2 & _CREG2_MASK_TM_EN)
        return val

    @time_measurement_enabled.setter
    def time_measurement_enabled(self, val):
        """ Enables/disables the conversion time measurement """
        with ConfigurationStateManager(self):
            if val:
                self.creg2 = self.creg2 | _CREG2_MASK_TM_ENV
            else:
                self.creg2 = self.creg2 & ~_CREG2_MASK_TM_EN

    @property
    def divider_enabled(self):
        """ 
        Reads CREG2 and return measurement divider enabled setting (True/False)
        """
        with ConfigurationStateManager(self):
            val = bool(self.creg2 & _CREG2_MASK_EN_DIV)
        return val

    @divider_enabled.setter
    def divider_enabled(self, val):
        """ Enables/disables the measurement divider """
        with ConfigurationStateManager(self):
            if val:
                self.creg2 = self.creg2 | _CREG2_MASK_EN_DIV
            else:
                self.creg2 = self.creg2 & ~_CREG2_MASK_EN_DIV
            self.state_copy['divider_enabled'] = self.divider_enabled

    @property
    def divider(self):
        """ Reads CREG2 and returns the measurement divider """
        with ConfigurationStateManager(self):
            val = self.creg2 & _CREG2_MASK_DIV
        return val

    @divider.setter
    def divider(self, new_div):
        """ Sets the measurement divider via CREG2 """
        with ConfigurationStateManager(self):
            if (new_div < _DIV_MIN_VAL) or (new_div > _DIV_MAX_VAL):
                raise ValueError(f'new_div out of range')
            self.creg2 = (self.creg2 & ~_CREG2_MASK_DIV) | new_div
            self.state_copy['divider'] = self.divider

    @property
    def measurement_mode(self):
        """
        Gets the current measurement mode from the CREG3 configuration register.

        Returns one of the following:
            MEASUREMENT_MODE_CONTINUOUS,
            MEASUREMENT_MODE_COMMAND,
            MEASUREMENT_MODE_SYNC_START,
            MEASUREMENT_MODE_SYNC_START_AND_END,
        """
        with ConfigurationStateManager(self):
            val = self.creg3 & _CREG3_MASK_MMODE
        return val

    @measurement_mode.setter
    def measurement_mode(self, new_mmode):
        """
        Sets the current measurement mode via the CREG3 configuration register.

        Can be set to one of the following:
            MEASUREMENT_MODE_CONTINUOUS,
            MEASUREMENT_MODE_COMMAND,
            MEASUREMENT_MODE_SYNC_START,
            MEASUREMENT_MODE_SYNC_START_AND_END,
        """
        with ConfigurationStateManager(self):
            if not new_mmode in ALLOWED_MEASUREMENT_MODES:
                raise ValueError(f'unknown measurement mode: {new_mmode}')
            self.creg3 = (self.creg3 & ~_CREG3_MASK_MMODE) | new_mmode
            self.state_copy['measurement_mode'] = new_mmode

    @property
    def measurement_mode_as_string(self):
        """
        Returns the current measurement mode from the CREG3 configuration register.

        Returns one of the following values.
            'continuous',        
            'command',           
            'sync_start',        
            'sync_start_and_end',
        """
        return MEASUREMENT_MODE_TO_STRING.get(self.measurement_mode, 'unknown')

    @property
    def standby_state(self):
        """
        Gets the standby state value from the CREG3 configuration register. 

        Returns True or False
        """
        with ConfigurationStateManager(self):
            val = bool(self.creg3 & _CREG3_MASK_SB)
        return val


    @standby_state.setter
    def standby_state(self, val):
        """
        Sets the standby state value in the CREG3 configuration register. 

        Can be set to either True or False
        """
        with ConfigurationStateManager(self):
            if val:
                self.creg3 = self.creg3 | _CREG3_MASK_SB
            else:
                self.creg3 = self.creg3 & ~_CREG3_MASK_SB

    @property
    def cclk(self):
        """
        Gets the internal clock frequency from the CREG3 configuratinon register

        Allowed values.
            CCLK_FREQ_1024KHZ
            CCLK_FREQ_2048KHZ
            CCLK_FREQ_4096KHZ
            CCLK_FREQ_8192KHZ
        """
        with ConfigurationStateManager(self):
            val = self.creg3 & _CREG3_MASK_CCLK
        return val

    @property
    def cclk_value(self):
        """
        Gets the internal clock frequency as a numeric value (kHz)
        """
        return cclk_to_value(self.cclk)

    @property
    def cclk_as_string(self):
        """
        Gets a the internal clock frequency as a string.
        """
        return f'{self.cclk_value:0.1f}kHz'

    @cclk.setter
    def cclk(self,new_cclk):
        """ 
        Sets the internal clock frequency via the CREG3 configuration register. 

        Allowed values.
            CCLK_FREQ_1024KHZ
            CCLK_FREQ_2048KHZ
            CCLK_FREQ_4096KHZ
            CCLK_FREQ_8192KHZ
        """
        with ConfigurationStateManager(self):
            if new_cclk < _CCLK_MIN_VAL or new_cclk > _CCLK_MAX_VAL: 
                raise ValueError(f'cclk out of range: {new_cclk}')
            self.creg3 = (self.creg3 & ~_CREG3_MASK_CCLK) | new_cclk
            self.state_copy['cclk'] = new_cclk

    @property
    def chip_id(self):
        """
        Reads the value of the chip id from the AGEN Register.
        """
        with ConfigurationStateManager(self):
            val = (self.read_uint8(_REG_ADDR_AGEN) & _AGEN_MASK_DEVID) >> _AGEN_SHIFT_DEVID 
        return val

    @property
    def conversion_factor(self):
        gain_value = gain_to_value(self.state_copy['gain'])
        time_value = integration_time_to_value(self.state_copy['integration_time'])
        cclk_value =  cclk_to_value(self.state_copy['cclk'])
        return 1.0/(gain_value*time_value*cclk_value)

    @property
    def divider_factor(self):
        if self.state_copy['divider_enabled']:
            div_factor = 1 << (1 + self.state_copy['divider'])
        else:
            div_factor = 1
        return div_factor

    @property
    def measurement_sleep_dt(self):
        return 0.001*integration_time_to_value(self.state_copy['integration_time'])

    @property
    def raw_values(self):
        self.start_measurement()
        time.sleep(self.measurement_sleep_dt)
        while self.notready:
            pass

        div_factor = self.divider_factor
        uva_raw = self.mres1_as_uint16*div_factor 
        uvb_raw = self.mres2_as_uint16*div_factor
        uvc_raw = self.mres3_as_uint16*div_factor
        temp_raw = self.temp_as_uint16

        if self.overflow_exception:
            if self.status_as_dict['mresof']:
                raise AS7331Overflow("measurement register overflow")

        return uva_raw, uvb_raw, uvc_raw, temp_raw

    @property
    def values(self):
        # Get conversion factors
        common_factor = self.conversion_factor
        conv_factor_a = _FSRA*common_factor
        conv_factor_b = _FSRB*common_factor
        conv_factor_c = _FSRC*common_factor

        # Get raw integer values and convert to uW/cm**2 or deg C
        uva_raw, uvb_raw, uvc_raw, temp_raw = self.raw_values
        uva = uva_raw*conv_factor_a
        uvb = uvb_raw*conv_factor_b
        uvc = uvc_raw*conv_factor_c
        temp = temp_raw_to_celsius(temp_raw)
        return uva, uvb, uvc, temp

# Exceptions
# -----------------------------------------------------------------------------

class AS7331Overflow(Exception):
    """
    Measurement overflow exception. Raised when there is an overflow in one of
    the MRESX measurement registers.
    """
    pass


# Context managers 
# -----------------------------------------------------------------------------

class ConfigurationStateManager:
    """
    Context manager for device configuration.  Puts the device into the 
    configuration state on enter and puts into the measurement state on
    exit.
    """

    def __init__(self, obj):
        self.obj = obj
        super().__init__()

    def __enter__(self):
        self.obj.device_state = DEVICE_STATE_CONFIGURATION

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.obj.device_state = DEVICE_STATE_MEASUREMENT


# Utility functions
# -----------------------------------------------------------------------------

def gain_to_value(gain):
    """
    Converts the gain setting to the gain multipler value.
    """
    return 1 << (11 - gain)

def integration_time_to_value(integration_time): 
    """
    Converts the integration time setting to the integration time value in ms.
    """
    return 1 << integration_time

def cclk_to_value(cclk):
    """
    Converts the cclk setting to the clock value in kHz.
    """
    return 1024.0*(1 << cclk)

def temp_raw_to_celsius(val):
    """
    Converts raw integer temperature reading to degress celsius as given
    on page 42 of the AS7331 specification document. 
    """
    return 0.05*val - 66.9

def bytes_to_uint16(lo_byte, hi_byte):
    """
    Converts two bytes to a uint16
    """
    return (hi_byte << 8) + lo_byte


