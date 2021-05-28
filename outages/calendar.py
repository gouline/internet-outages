import logging
from typing import List
import ics

from .outage import Outage


def write_calendar(outages: List[Outage], filename: str):
    """Writes list of outages into iCal format.

    Args:
        outages (List[Outage]): List of outages.
        filename (str): File path to write to.
    """

    cal = ics.Calendar()

    for outage in outages:
        event = ics.Event(
            name=outage.name,
            begin=outage.start.timestamp() if outage.start else None,
            end=outage.end.timestamp() if outage.end else None,
            uid=outage.uid,
            description=outage.description(),
        )
        cal.events.add(event)
        logging.info("Calendar event: %s", event)

    logging.info("Calendar generated")

    with open(filename, "w") as f:
        f.writelines(cal)
        logging.info("Calendar written")
