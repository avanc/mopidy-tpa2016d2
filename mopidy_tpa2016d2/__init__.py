from __future__ import unicode_literals

import os

from mopidy import config, ext


__version__ = '0.0.1'


class Extension(ext.Extension):
    dist_name = 'Mopidy-TPA2016D2'
    ext_name = 'tpa2016d2'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['i2c_bus'] = config.Integer()
        return schema

    def setup(self, registry):
        from .mixer import TPA2016D2Mixer

        registry.add('mixer', TPA2016D2Mixer)
