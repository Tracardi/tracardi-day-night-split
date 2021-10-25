from datetime import datetime
from typing import Tuple

from geopy import Nominatim, GoogleV3, Bing
from astral import LocationInfo
from astral.sun import sun
import pytz


def day_night_split(town: str, time_now: datetime, service="open-street-map", agent="Tracardi") -> Tuple[
    datetime, datetime]:
    if service == "open-street-map":
        locator = Nominatim(user_agent=agent)
    elif service == "google-map":
        locator = GoogleV3(api_key="None",user_agent=agent)
    elif service == "bing":
        locator = Bing(api_key="None", user_agent=agent)
    else:
        raise ValueError("Undefined location service. Available [\"open-street-map\",\"google-map\", \"bing\"]")

    location = locator.geocode(town)

    loc_info = LocationInfo(latitude=location.latitude, longitude=location.longitude)

    sun_info = sun(loc_info.observer, date=time_now)

    return sun_info['sunrise'], sun_info['sunset']


def is_day(town, service="open-street-map"):
    now = datetime.now()

    utc = pytz.UTC
    now = now.replace(tzinfo=utc)

    sun_rise, sun_set = day_night_split(town, now, service=service)

    return sun_rise < now < sun_set
