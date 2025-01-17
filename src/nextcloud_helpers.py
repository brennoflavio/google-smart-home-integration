from variables import load_and_assert
import caldav
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import urllib.parse
import requests


def create_ical_card(summary, due_date=None):
    dt = datetime.now(tz=timezone(timedelta(hours=-3)))
    parsed_dt = dt.strftime("%Y%m%dT%H%M%S")
    ical_base = f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Smart Home Integration
BEGIN:VTODO
UID:{str(uuid4())}
CREATED:{parsed_dt}
LAST-MODIFIED:{parsed_dt}
DTSTAMP:{parsed_dt}
SUMMARY:{summary}
"""
    if due_date:
        parsed_tomorrow = due_date.strftime("%Y%m%d")
        ical_base = f"{ical_base}DUE;VALUE=DATE:{parsed_tomorrow}\n"
        ical_base = f"{ical_base}DTSTART;VALUE=DATE:{parsed_tomorrow}\n"

    ical_base = f"{ical_base}END:VTODO\n"
    ical_base = f"{ical_base}END:VCALENDAR\n"

    return ical_base.strip()


def create_task(
    summary, due=None, task_list_name=load_and_assert("NEXTCLOUD_TASK_LIST_NAME")
):
    client = caldav.DAVClient(
        url=load_and_assert("NEXTCLOUD_CALENDAR_URL"),
        username=load_and_assert("NEXTCLOUD_USERNAME"),
        password=load_and_assert("NEXTCLOUD_PASSWORD"),
    )

    principal = client.principal()
    calendar = principal.calendar(name=task_list_name)

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


def create_note(title, content):
    url = urllib.parse.urljoin(
        load_and_assert("NEXTCLOUD_URL"), "index.php/apps/notes/api/v1/notes"
    )

    if not title:
        if len(content) >= 30:
            title = content[:30]
        else:
            title = content

    response = requests.post(
        url,
        auth=(
            load_and_assert("NEXTCLOUD_USERNAME"),
            load_and_assert("NEXTCLOUD_PASSWORD"),
        ),
        json={
            "title": title,
            "content": content,
        },
    )

    response.raise_for_status()
