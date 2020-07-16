import numpy as np

import matplotlib.pyplot as plt

from astropy.visualization import astropy_mpl_style, quantity_support
from astropy.coordinates import get_sun, get_moon, SkyCoord, EarthLocation, AltAz
import astropy.units as u
from astropy.time import Time

from astroquery.mpc import MPC

from datetime import datetime, timedelta

# Set plot style
plt.style.use(astropy_mpl_style)
quantity_support()

# Based on: https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html

# Settings for observing location
LATITUDE = 56.15
LONGITUDE = -3.74
HEIGHT = 50
UTC_OFFSET = +1

# Get the datetime of midnight tonight
date_tomorrow = datetime.today() + timedelta(days=1)
next_midnight = date_tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

# Find NEOWISE in the MPC database
# result = MPC.query_object('comet', designation='C/2020 F3')

# Get the NEOWISE ephemeris data for midnight from the Minor Planet Ephemeris Service
neo_ephemeris = MPC.get_ephemeris('C/2020 F3', start=next_midnight, number=1)
print(neo_ephemeris['Date'][0])
print(neo_ephemeris['RA'][0])
print(neo_ephemeris['Dec'][0])

# Extract the RA and Dec from the ephemeris data
neowise_ra = neo_ephemeris['RA'][0]
neowise_dec = neo_ephemeris['Dec'][0]

# Define the location in the sky of C/2020 F3 NEOWISE based on the RA and Dec from the Ephemeris
neowise = SkyCoord(neowise_ra, neowise_dec, frame='icrs', unit='deg')

# Set the observing location based on the lat, long and height defined in settings
observing_location = EarthLocation(lat=LATITUDE * u.deg, lon=LONGITUDE * u.deg, height=HEIGHT * u.m)

# Apply the offset from settings
utcoffset = UTC_OFFSET * u.hour  # BST
midnight = Time(next_midnight) - utcoffset

# Get 1000 evenly spaced times for the twelve hours around midnight (6pm to 6am)
delta_midnight = np.linspace(-6, 6, 1000) * u.hour
times_today_tomorrow = midnight + delta_midnight

# Use the times and observing location to set an observing frame - this will be used for the objects of interest
frame_today_tomorrow = AltAz(obstime=times_today_tomorrow, location=observing_location)

# Use get_sun and get_moon to find the alt-az of the Sun and Moon over the observing period
sunaltazs_today_tomorrow = get_sun(times_today_tomorrow).transform_to(frame_today_tomorrow)
moonaltazs_today_tomorrow = get_moon(times_today_tomorrow).transform_to(frame_today_tomorrow)

# Find the alt-az coordinates of NEOWISE over the observing period
neowise_altazs_today_tomorrow = neowise.transform_to(frame_today_tomorrow)

# Make a nice plot of the sun, moon and comet, along with visual indication of twilights
plt.plot(delta_midnight, sunaltazs_today_tomorrow.alt, color='y', ls='--', label='Sun')
plt.plot(delta_midnight, moonaltazs_today_tomorrow.alt, color=[0.75] * 3, ls='--', label='Moon')
plt.scatter(delta_midnight, neowise_altazs_today_tomorrow.alt,
            c=neowise_altazs_today_tomorrow.az, label='C/2020 F3 NEOWISE', lw=0, s=8,
            cmap='twilight_shifted')
plt.fill_between(delta_midnight, 0 * u.deg, 90 * u.deg,
                 sunaltazs_today_tomorrow.alt < -0 * u.deg, color='#65B4CF', zorder=0)
plt.fill_between(delta_midnight, 0 * u.deg, 90 * u.deg,
                 sunaltazs_today_tomorrow.alt < -6 * u.deg, color='#316677', zorder=0)
plt.fill_between(delta_midnight, 0 * u.deg, 90 * u.deg,
                 sunaltazs_today_tomorrow.alt < -12 * u.deg, color='#1B404D', zorder=0)
plt.fill_between(delta_midnight, 0 * u.deg, 90 * u.deg,
                 sunaltazs_today_tomorrow.alt < -18 * u.deg, color='k', zorder=0)
plt.colorbar().set_label('Azimuth [deg]')
plt.legend(loc='upper left')
plt.xlim(-6 * u.hour, 6 * u.hour)
plt.xticks((np.arange(13) * 1 - 6) * u.hour)
plt.ylim(0 * u.deg, 90 * u.deg)
plt.xlabel('Hours from BST Midnight')
plt.ylabel('Altitude [deg]')
# plt.show()

filename = 'neowise-{}.png'.format(datetime.strftime(next_midnight, '%Y-%m-%d'))
plt.savefig(filename, bbox_inches='tight')
