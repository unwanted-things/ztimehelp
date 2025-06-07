import datetime
from typing import Dict
import pytz
from datetime import timezone
from ztimehelp.config import config


def get_date_object(date: datetime.date, change_timezone=True) -> Dict[str, str]:
    ist_tz = pytz.timezone(config.get("TIME_ZONE"))

    start_date_ist = datetime.datetime.combine(date, datetime.time.min)
    end_date_ist = datetime.datetime.combine(date, datetime.time.max)

    if not change_timezone:
        return {
            "start_date": end_date_ist,
            "end_date": end_date_ist + datetime.timedelta(days=1),
        }

    start_date_ist = ist_tz.localize(start_date_ist)
    end_date_ist = ist_tz.localize(end_date_ist)

    start_date_utc = start_date_ist.astimezone(pytz.UTC)
    end_date_utc = end_date_ist.astimezone(pytz.UTC)

    return {"start_date": start_date_utc, "end_date": end_date_utc}
