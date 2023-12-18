from variables import load_and_assert
import caldav
from datetime import datetime, timezone, timedelta
from uuid import uuid4


def create_ical_card(summary, due_date):
    dt = datetime.now(tz=timezone(timedelta(hours=-3)))
    parsed_dt = dt.strftime("%Y%m%dT%H%M%S")
    parsed_tomorrow = due_date.strftime("%Y%m%d")
    ical_base = f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Nextcloud Alexa
BEGIN:VTODO
UID:{str(uuid4())}
CREATED:{parsed_dt}
LAST-MODIFIED:{parsed_dt}
DTSTAMP:{parsed_dt}
SUMMARY:{summary}
DUE;VALUE=DATE:{parsed_tomorrow}
DTSTART;VALUE=DATE:{parsed_tomorrow}
END:VTODO
END:VCALENDAR
    """
    return ical_base.strip()


def create_task(summary, due):
    client = caldav.DAVClient(
        url=load_and_assert("NEXTCLOUD_CALENDAR_URL"),
        username=load_and_assert("NEXTCLOUD_USERNAME"),
        password=load_and_assert("NEXTCLOUD_PASSWORD"),
    )

    principal = client.principal()
    calendar = principal.calendar(name=load_and_assert("NEXTCLOUD_TASK_LIST_NAME"))

    ical = create_ical_card(summary, due)
    calendar.add_event(ical)


def create_calendar_event(start_date, end_date, summary):
    client = caldav.DAVClient(
        url=load_and_assert("NEXTCLOUD_CALENDAR_URL"),
        username=load_and_assert("NEXTCLOUD_USERNAME"),
        password=load_and_assert("NEXTCLOUD_PASSWORD"),
    )

    principal = client.principal()
    calendar = principal.calendar(name=load_and_assert("NEXTCLOUD_CALENDAR_NAME"))
    calendar.save_event(
        dtstart=start_date,
        dtend=end_date,
        summary=summary,
    )
