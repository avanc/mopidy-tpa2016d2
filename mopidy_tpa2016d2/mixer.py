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

        self._volume_cache = 0
        self._tpa2016d2_talker = None

    def get_volume(self):
        return self._volume_cache

    def set_volume(self, volume):
        self._volume_cache = volume
        self._tpa2016d2_talker.set_volume(volume)
        self.trigger_volume_changed(volume)

    def get_mute(self):
        return False

    def set_mute(self, mute):
        self._tpa2016d2_talker.mute(mute)
        self.trigger_mute_changed(mute)

    def on_start(self):
        self._start_tpa2016d2_talker()

    def _start_tpa2016d2_talker(self):
        self._tpa2016d2_talker = talker.TPA2016D2Talker.start(i2c_bus=self.i2c_bus).proxy()
        self._volume_cache = self._tpa2016d2_talker.get_volume().get()
