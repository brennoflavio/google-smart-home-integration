import google_helpers
import nextcloud_helpers as nextcloud_helpers
from variables import load, load_and_assert


def sync_shopping_list():
    shopping_list = google_helpers.get_shopping_list(load("NEXTCLOUD_LIST_REGEX"))

    for item in shopping_list:
        nextcloud_helpers.create_task(
            item, task_list_name=load_and_assert("NEXTCLOUD_SHOPPING_LIST_NAME")
        )

    google_helpers.clear_shopping_list(load("NEXTCLOUD_LIST_REGEX"))


def sync_notes():
    notes = google_helpers.get_notes(load("NEXTCLOUD_LIST_REGEX"))

    for note in notes:
        title = note["title"]
        text = note["text"]
        nextcloud_helpers.create_note(title, text)

    google_helpers.clear_notes(load("NEXTCLOUD_LIST_REGEX"))


if __name__ == "__main__":
    sync_shopping_list()
    sync_notes()
