from googleapiclient.discovery import build
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
from variables import load_and_assert
import caldav
from dateutil.parser import parse


def register_calendar(service):
    calendar_list_entry = {"id": load_and_assert("CALENDAR_ID")}

    created_calendar_list_entry = (
        service.calendarList().insert(body=calendar_list_entry).execute()
    )
    print(created_calendar_list_entry)


def get_google_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        load_and_assert("KEY_FILE_NAME"),
        scopes=["https://www.googleapis.com/auth/calendar"],
    )
    service = build("calendar", "v3", credentials=credentials)
    return service


def list_calendar_events(service):
    ts = (
        datetime.utcnow() - timedelta(days=30)
    ).isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=load_and_assert("CALENDAR_ID"),
            timeMin=ts,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result


def create_nextcloud_calendar_event(start_date, end_date, summary):
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


def parse_google_calendar_json(data):
    start_str = data.get("start", {}).get("dateTime") or data.get("start", {}).get(
        "date"
    )
    end_str = data.get("end", {}).get("dateTime") or data.get("end", {}).get("date")
    summary = data.get("summary")
    id = data.get("id")

    if not start_str or not end_str or not summary or not id:
        return None, None, ""

    return parse(start_str), parse(end_str), summary.strip(), id


def delete_google_event(id, service):
    service.events().delete(
        calendarId=load_and_assert("CALENDAR_ID"), eventId=id
    ).execute()


def main():
    service = get_google_service()
    events_result = list_calendar_events(service)

    for event in events_result.get("items", []):
        start, end, summary, id = parse_google_calendar_json(event)
        if not start or not end or not summary or not id:
            continue

        create_nextcloud_calendar_event(start, end, summary)
        delete_google_event(id, service)


if __name__ == "__main__":
    main()
