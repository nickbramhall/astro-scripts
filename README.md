# astro-scripts
Miscellaneous scripts for astronomy related activities

## comet_neo.py

This script returns an observing plan for Comet C/2020 F3 NEOWISE based on a given location for the hours centred around local midnight. It is configured for my location in Scotland but the latitude, longitude, altitude and UTC offset can be updated to suit.

<a href="https://www.flickr.com/photos/black_friction/50122818132/in/datetaken/" title="Comet NEOWISE"><img src="https://live.staticflickr.com/65535/50122818132_2e7a3b2a2f.jpg" width="500" height="387" alt="Comet NEOWISE"></a>

The script gets ephemeris data for the comet and plots the changing altitude of the comet over the night along with the altitude of the sun and moon. In addition, the various twilights are shown based on the angle of the sun below the horizon.
