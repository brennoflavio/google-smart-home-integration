import google_helpers
import nextcloud_helpers as nextcloud_helpers


def sync_events():
    events = google_helpers.getlist_calendar_events()

    for event in events:
        start = event.get("start")
        end = event.get("end")
        summary = event.get("summary")
        id = event.get("id")

        nextcloud_helpers.create_calendar_event(start, end, summary)
        google_helpers.delete_calendar_event(id)


if __name__ == "__main__":
    sync_events()
