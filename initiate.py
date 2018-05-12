
from pymongo import MongoClient
import scrape_mars  

client = MongoClient("mongodb://localhost:27017")
db = client.mission_to_mars

output ={
 'facts': {'Equatorial Diameter:': '6,792 km\n',
  'First Record:': '2nd millennium BC',
  'Mass:': '6.42 x 10^23 kg (10.7% Earth)',
  'Moons:': '2 (Phobos & Deimos)',
  'Orbit Distance:': '227,943,824 km (1.52 AU)',
  'Orbit Period:': '687 days (1.9 years)\n',
  'Polar Diameter:': '6,752 km\n',
  'Recorded By:': 'Egyptian astronomers',
  'Surface Temperature: ': '-153 to 20 °C'},
 'featured_image_url': 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18452_ip.jpg',
 'hemisphere_image_urls': [{'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg',
   'title': 'Cerberus Hemisphere Enhanced'},
  {'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg',
   'title': 'Schiaparelli Hemisphere Enhanced'},
  {'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg',
   'title': 'Syrtis Major Hemisphere Enhanced'},
  {'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg',
   'title': 'Valles Marineris Hemisphere Enhanced'}],
 'news': {'news_p': "MarCO is a pair of tiny spacecraft that launched with NASA's InSight lander today.",
  'news_title': "NASA's First Deep-Space CubeSats Say: 'Polo!'"},
 'weather': 'Sol 2043 (May 06, 2018), Sunny, high -14C/6F, low -71C/-95F, pressure at 7.36 hPa, daylight 05:22-17:20'}

output = scrape_mars.scrape() 
db.general.insert_one(output)