from datetime import datetime


class Outage:
    """Generic container for outages."""

    def __init__(
        self,
        uid=None,
        name="",
        start: datetime = None,
        end: datetime = None,
        summary="",
        severity="",
    ):
        self.uid = uid
        self.name = name
        self.start = start
        self.end = end
        self.summary = summary
        self.severity = severity

    def description(self) -> str:
        """Generate description body from fields.

        Returns:
            str: Text-only description.
        """

        return f"Severity: {self.severity}\n{self.summary}"

    def __repr__(self) -> str:
        return (
            f"Outage("
            + f"start={self.start}"
            + f", end={self.end}"
            + f", summary={self.summary}"
            + f", severity={self.severity}"
            + f")"
        )
