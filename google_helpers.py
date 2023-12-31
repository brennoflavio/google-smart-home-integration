from googleapiclient.discovery import build
from variables import load_and_assert
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from dateutil.parser import parse
from datetime import datetime, timedelta
import gkeepapi

SCOPES = [
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/calendar",
]


def get_credentials():
    user_file = load_and_assert("GOGLE_AUTHORIZED_USER_FILE")
    if os.path.exists(user_file):
        creds = Credentials.from_authorized_user_file(user_file, SCOPES)
        return creds
    return None


def get_authorization_url(redirect_url):
    flow = Flow.from_client_secrets_file(
        load_and_assert("GOOGLE_OAUTH_SECRET_FILE"),
        scopes=SCOPES,
        redirect_uri=redirect_url,
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    return authorization_url, state


def handle_callback(state, redirect_url, request_url):
    flow = Flow.from_client_secrets_file(
        load_and_assert("GOOGLE_OAUTH_SECRET_FILE"),
        scopes=SCOPES,
        state=state,
        redirect_uri=redirect_url,
    )
    flow.fetch_token(authorization_response=request_url)
    creds = flow.credentials
    with open(load_and_assert("GOGLE_AUTHORIZED_USER_FILE"), "w+") as token:
        token.write(creds.to_json())


def get_tasks_service():
    credentials = get_credentials()
    service = build("tasks", "v1", credentials=credentials)
    return service


def get_calendar_service():
    credentials = get_credentials()
    service = build("calendar", "v3", credentials=credentials)
    return service


def get_tasklist_id():
    service = get_tasks_service()
    results = service.tasklists().list().execute()
    tasklist_id = [
        x["id"]
        for x in results.get("items", [])
        if x["title"] == load_and_assert("GOOGLE_TASKLIST_NAME")
    ]
    if tasklist_id:
        return tasklist_id[0]
    else:
        return None


def get_tasks(result_number=50):
    service = get_tasks_service()
    tasklist_id = get_tasklist_id()

    tasks = (
        service.tasks()
        .list(tasklist=tasklist_id, maxResults=result_number, showCompleted=False)
        .execute()
    )
    tasks = tasks.get("items", [])

    return [
        {
            "id": x["id"],
            "due": parse(x["due"]) if x.get("due") else None,
            "title": x["title"],
        }
        for x in tasks
    ]


def delete_task(task_id):
    service = get_tasks_service()
    tasklist_id = get_tasklist_id()
    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()


def parse_google_calendar_json(data):
    start_str = data.get("start", {}).get("dateTime") or data.get("start", {}).get(
        "date"
    )
    end_str = data.get("end", {}).get("dateTime") or data.get("end", {}).get("date")
    summary = data.get("summary")
    id = data.get("id")

    if not start_str or not end_str or not summary or not id:
        return None, None, ""

    return {
        "start": parse(start_str),
        "end": parse(end_str),
        "summary": summary.strip(),
        "id": id,
    }


def getlist_calendar_events():
    service = get_calendar_service()
    ts = (
        datetime.utcnow() - timedelta(days=30)
    ).isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=load_and_assert("GOOGLE_CALENDAR_ID"),
            timeMin=ts,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    final = []
    for row in events_result.get("items", []):
        final.append(parse_google_calendar_json(row))

    return final


def delete_calendar_event(id):
    service = get_calendar_service()
    service.events().delete(
        calendarId=load_and_assert("GOOGLE_CALENDAR_ID"), eventId=id
    ).execute()


def get_keep_service():
    keep = gkeepapi.Keep()
    keep.resume(
        load_and_assert("GOOGLE_KEEP_USER"), load_and_assert("GOOGLE_KEEP_MASTER_TOKEN")
    )
    return keep


def get_shopping_list():
    service = get_keep_service()
    lists = [
        x
        for x in service.all()
        if isinstance(x, gkeepapi.node.List)
        and x.title == load_and_assert("GOOGLE_KEEP_SHOPPINGLIST_NAME")
    ]
    shopping_list = lists[0]
    return [x.text for x in shopping_list.unchecked]


def clear_shopping_list():
    service = get_keep_service()
    lists = [
        x
        for x in service.all()
        if isinstance(x, gkeepapi.node.List)
        and x.title == load_and_assert("GOOGLE_KEEP_SHOPPINGLIST_NAME")
    ]
    shopping_list = lists[0]

    for item in shopping_list.items:
        item.delete()

    service.sync()


def get_notes():
    service = get_keep_service()
    notes = [x for x in service.all() if isinstance(x, gkeepapi.node.Note)]
    return [
        {
            "title": x.title,
            "text": x.text,
        }
        for x in notes
    ]


def clear_notes():
    service = get_keep_service()
    notes = [x for x in service.all() if isinstance(x, gkeepapi.node.Note)]
    for note in notes:
        note.delete()
    service.sync()
