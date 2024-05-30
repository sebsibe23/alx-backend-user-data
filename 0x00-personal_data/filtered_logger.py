#!/usr/bin/env python3
"""
A module for filtering logs containing Personally Identifiable
Information (PII). It provides functions to filter log lines,
create loggers, and connect to a database.
"""
import os
import re
import logging
import mysql.connector
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format(
        '|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Filters a log line to redact specified fields.

    Args:
        fields (List[str]): List of fields to redact.
        redaction (str): Redaction string.
        message (str): Log message.
        separator (str): Field separator.

    Returns:
        str: Redacted log message.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    try:
        return re.sub(extract(fields, separator), replace(redaction),
                      message)
    except re.error as e:
        logging.error("Regex error: %s", e)
        return message


def get_logger() -> logging.Logger:
    """
    Creates a new logger for user data.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to a MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection.
    """
    try:
        db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
        db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
        db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
        db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
        connection = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_pwd,
            database=db_name,
        )
        return connection
    except mysql.connector.Error as err:
        logging.error("Database connection error: %s", err)
        return None


def main():
    """
    Logs the information about user records in a table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    record = map(
                        lambda x: '{}={}'.format(x[0], x[1]),
                        zip(columns, row),
                    )
                    msg = '{};'.format('; '.join(list(record)))
                    args = ("user_data", logging.INFO, None, None, msg,
                            None, None)
                    log_record = logging.LogRecord(*args)
                    info_logger.handle(log_record)
        except mysql.connector.Error as err:
            logging.error("Database query error: %s", err)
        finally:
            connection.close()
    else:
        logging.error("No database connection available")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class to redact PII fields.
    """
    REDACTION = "***"
    FORMAT = ("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: "
              "%(message)s")
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a LogRecord, redacting specified fields.

        Args:
            record (logging.LogRecord): Log record to format.

        Returns:
            str: Formatted and redacted log record.
        """
        try:
            msg = super(RedactingFormatter, self).format(record)
            txt = filter_datum(self.fields, self.REDACTION, msg,
                               self.SEPARATOR)
            return txt
        except Exception as e:
            logging.error("Formatting error: %s", e)
            return record.getMessage()


if __name__ == "__main__":
    main()
