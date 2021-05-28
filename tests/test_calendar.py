from datetime import datetime, timezone
import unittest
import os

from outages.calendar import write_calendar
from outages.outage import Outage

OUTPUT_DIR = os.path.join("build", "test", "calendar")


class TestCalendar(unittest.TestCase):
    def setUp(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def test_empty(self):
        filename = os.path.join(OUTPUT_DIR, "test_empty.ics")
        write_calendar([], filename)

        with open(filename, "r") as f:
            actual = f.read()

        self.assertEqual(
            actual,
            """BEGIN:VCALENDAR
VERSION:2.0
PRODID:ics.py - http://git.io/lLljaA
END:VCALENDAR
""",
        )

    def test_payload(self):
        filename = os.path.join(OUTPUT_DIR, "test_payload.ics")
        write_calendar(
            [
                Outage(
                    uid="TEST-UID-1",
                    name="Event Name 1",
                    start=datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
                ),
                Outage(
                    uid="TEST-UID-2",
                    name="Event Name 2",
                    start=datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
                    end=datetime(2021, 1, 2, 0, 0, 0, 0, tzinfo=timezone.utc),
                    summary="Summary 1",
                    severity="Low",
                ),
            ],
            filename,
        )

        with open(filename, "r") as f:
            actual = f.read()

        self.assertEqual(
            actual,
            """BEGIN:VCALENDAR
VERSION:2.0
PRODID:ics.py - http://git.io/lLljaA
BEGIN:VEVENT
DESCRIPTION:Severity: \\n
DTSTART:20210101T000000Z
SUMMARY:Event Name 1
UID:TEST-UID-1
END:VEVENT
BEGIN:VEVENT
DESCRIPTION:Severity: Low\\nSummary 1
DTEND:20210102T000000Z
DTSTART:20210101T000000Z
SUMMARY:Event Name 2
UID:TEST-UID-2
END:VEVENT
END:VCALENDAR
""",
        )
