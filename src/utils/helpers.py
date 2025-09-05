# Utility functions for the Intelligent Productivity Assistant

from datetime import datetime
import logging

def setup_logging(log_file='app.log'):
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def parse_date(date_string, date_format='%Y-%m-%d'):
    """Parse a date string into a datetime object."""
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        return None

def format_date(date_obj, date_format='%Y-%m-%d'):
    """Format a datetime object into a string."""
    return date_obj.strftime(date_format) if date_obj else None

def log_info(message):
    """Log an informational message."""
    logging.info(message)

def log_error(message):
    """Log an error message."""
    logging.error(message)