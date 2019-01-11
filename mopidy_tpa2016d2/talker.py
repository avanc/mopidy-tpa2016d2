import logging

import pykka

import smbus

logger = logging.getLogger(__name__)

SETUP=0x1
SETUP_SPK_EN_R=0x80
SETUP_SPK_EN_L=0x40
SETUP_SWS=0x20
#define TPA2016_SETUP_R_FAULT 0x10
#define TPA2016_SETUP_L_FAULT 0x08
#define TPA2016_SETUP_THERMAL 0x04
#define TPA2016_SETUP_NOISEGATE 0x01
#define TPA2016_ATK 0x2
#define TPA2016_REL 0x3
#define TPA2016_HOLD 0x4
GAIN=0x5


class TPA2016D2Talker(pykka.ThreadingActor):
    """
    Independent thread which does the communication with the TDA2016 amplifier.

    Since the communication is done in an independent thread, Mopidy won't
    block other requests while sending commands to the receiver.
    """

    _min_volume = -28
    _max_volume = 30
    _i2c_address = 0x58

    def __init__(self, i2c_bus):
        super(TPA2016D2Talker, self).__init__()

        self.address = self._i2c_address
        self.bus = smbus.SMBus(i2c_bus)

    def on_start(self):
        self._set_device_to_known_state()

    def _set_device_to_known_state(self):
        self.mute(False)

    def mute(self, mute=None):
        data = self.bus.read_byte_data(self.address, SETUP)
        
        if (mute is None):
            mute = not (data & (SETUP_SPK_EN_L|SETUP_SPK_EN_R))
        else:
            if (mute):
                data &= ~SETUP_SPK_EN_L
                data &= ~SETUP_SPK_EN_R
            else:
                data |= SETUP_SPK_EN_L
                data |= SETUP_SPK_EN_R
            self.bus.write_byte_data(self.address, SETUP, data)
            
        return mute
        

    def _get_volume(self):
        volume = self.bus.read_byte_data(self.address, GAIN)
        if (volume>31):
            volume = - ((volume^63)+1)
        percentage_volume = int( round( (
            (volume - self._min_volume)
            / float(self._max_volume - self._min_volume)
            ) * 100 ) )
        logger.debug(
            'TDA2016D2 amplifier: Volume is "%d" (%d%%)',
            volume, percentage_volume)
        return percentage_volume


    def _set_volume(self, percentage_volume):
        volume = ( percentage_volume / 100.0 * (self._max_volume-self._min_volume)
            ) + self._min_volume
        volume = int(round(volume))
        logger.debug(
            'TDA2016D2 amplifier: Set volume to "%d" (%d%%)',
            volume, percentage_volume)
        
        if (volume<0):
            volume = ((-volume)^63)+1

        self.bus.write_byte_data(self.address, GAIN, volume)

        return True

    def volume(self, volume=None):
        if (volume is None):
            volume = self._get_volume()
        else:
            self._set_volume(volume)
        
        return volume
       
       
        
