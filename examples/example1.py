import sys
sys.path.append('src')

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


count = 0
while True:

    if 1:
        try:
            uva, uvb, uvc, temp = sensor.values
        except as7331.AS7331Overflow as err:
            print('A')
            print(err)
        else:
            print(f'uva: {uva:1.2f}, uvb: {uvb:1.2f}, uvc: {uvc:1.2f}, temp: {temp:1.2f}')

    if 0:
        try:
            rawa, rawb, rawc, raw_temp = sensor.raw_values
        except as7331.AS7331Overflow as err:
            print('B')
            print(err)
        else:
            print(f'rawa: {rawa}, rawb: {rawb}, rawc: {rawc}, raw_temp: {raw_temp}')

    print()
