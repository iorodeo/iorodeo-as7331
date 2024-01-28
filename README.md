## iorodeo-as7331

Circuitpython library for the AS7331 Spectral UV sensor.  Implements I2C an
interface with the AS7331 sensor. Currently only supports the "command"
measurement mode.  The other modes "continuous", "synchronos" could probably be
added with a little effort.


### Requirements
adafruit\_bus\_device

### Usage

```python
    import time
    import board
    import iorodeo_as7331 as as7331
    
    i2c = board.I2C()
    sensor = as7331.AS7331(i2c)

    sensor.gain = as7331.GAIN_512X
    sensor.integration_time = as7331.INTEGRATION_TIME_128MS

    print(f'chip id:            {sensor.chip_id}')
    print(f'device state:       {sensor.device_state_as_string}')
    print(f'gain_as_string:     {sensor.gain_as_string}')
    print(f'integration_time:   {sensor.integration_time_as_string}')
    print(f'divider enabled:    {sensor.divider_enabled}')
    print(f'divider:            {sensor.divider}')
    print(f'power_down_enable:  {sensor.power_down_enable}')
    print(f'standby state:      {sensor.standby_state}')
    print(f'gain:               {sensor.gain_as_string}')
    print('-'*60)
    
    
    while True:
        uva, uvb, uvc, temp = sensor.values
        print(f'uva: {uva:1.2f}, uvb: {uvb:1.2f}, uvc: {uvc:1.2f}, temp: {temp:1.2f}')
        time.sleep(0.1)
    
```








