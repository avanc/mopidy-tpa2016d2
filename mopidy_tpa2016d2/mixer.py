"""Mixer that controls volume using TPA2016D2."""

from __future__ import unicode_literals

import logging

from mopidy import mixer

import pykka

from mopidy_tpa2016d2 import talker


logger = logging.getLogger(__name__)


class TPA2016D2Mixer(pykka.ThreadingActor, mixer.Mixer):

    name = 'tpa2016d2'

    def __init__(self, config):
        super(TPA2016D2Mixer, self).__init__(config)

        self.i2c_bus = config['tpa2016d2']['i2c_bus']

        self._tpa2016d2_talker = None

    def get_volume(self):
        return self._tpa2016d2_talker.volume().get()

    def set_volume(self, volume):
        self._tpa2016d2_talker.volume(volume)
        self.trigger_volume_changed(volume)

    def get_mute(self):
        return self._tpa2016d2_talker.mute().get()

    def set_mute(self, mute):
        self._tpa2016d2_talker.mute(mute)
        self.trigger_mute_changed(mute)

    def on_start(self):
        self._tpa2016d2_talker = talker.TPA2016D2Talker.start(i2c_bus=self.i2c_bus).proxy()
