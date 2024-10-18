import datetime
import re

from interview.core.exceptions import TMTBadRequestParamError

def convert_date(
    date_str: str | datetime.date,
    date_name: str | None = None,
    mask: bool = True
) -> datetime.date:
    """
    NOTE: Do not use this in a view to validate/convert a date from a request payload.
    Use convert_date_from_request instead.

    Convert a date string to a Python datetime.date
    :param date_str: Date string
    :param date_name: Name of the date, e.g. "start date"
    :param mask: Whether to mask the date in error message
    :return: The date
    :raises ValueError: If the given value doesn't conform to any of the date formats
    """
    if isinstance(date_str, datetime.date):
        return date_str

    date_str = str(date_str)
    for date_format in (
        "%Y-%m-%d",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%m.%d.%Y",
        "%b %d, %Y",
        "%B %d, %Y",
    ):
        try:
            return datetime.datetime.strptime(date_str, date_format).date()
        except ValueError:
            pass

    date_name = date_name.capitalize() if date_name else "Date"

    # Mask all the digits with * in-case the date is sensitive, e.g. patient's dob
    date_str = re.sub(r"\d", "*", date_str) if mask else date_str

    message = (
        f"{date_name} must be in YYYY-MM-DD, MM/DD/YYYY, MM-DD-YYYY, "
        f'"MMMM DD, YYYY" or MM.DD.YYYY format. Got date: {date_str}.'
    )

    raise ValueError(message)


def convert_date_from_request(
    date: str | datetime.date, date_name: str | None = None
) -> datetime.date:
    """
    NOTE: Use in view to validate date from request payload.

    :param date: nate string
    :param date_name: name of the date, e.g. "start date"
    :return: the date
    :raises ValidationError: (which is handled by api_view_logger) if the
        given value doesn't conform to any of the date formats
    """
    try:
        return convert_date(date_str=date, date_name=date_name, mask=False)
    except ValueError as e:
        raise TMTBadRequestParamError(e) from e
