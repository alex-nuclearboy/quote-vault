import os
import logging

# Define the directory for storing logs
LOG_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../../logs'
)


def ensure_log_directory_exists(directory: str) -> None:
    """
    Ensure that the log directory exists. If not, create it.

    :param directory: The path to the log directory.
    :type directory: str
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def setup_logger(
        name: str, log_file_name: str = 'scraper.log',
        log_level: int = logging.DEBUG
) -> logging.Logger:
    """
    Set up a logger with the given name.

    Logs will be written to a file in the 'logs' directory
    and also displayed in the console.

    :param name: The name of the logger (typically the module name).
    :type name: str
    :param log_file_name: The name of the log file. Defaults to 'scraper.log'.
    :type log_file_name: str, optional
    :param log_level: The logging level (e.g., logging.DEBUG, logging.INFO).
                      Defaults to logging.DEBUG.
    :type log_level: int, optional
    :return: Configured logger instance.
    :rtype: logging.Logger
    """
    # Ensure the log directory exists
    ensure_log_directory_exists(LOG_DIR)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create a stream handler for console output
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create a file handler for writing logs to a file
    log_file_path = os.path.join(LOG_DIR, log_file_name)
    fh = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    fh.setLevel(log_level)

    # Define log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
