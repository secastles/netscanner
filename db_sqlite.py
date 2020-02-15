import sqlite3
from sqlite3 import Error
from pathlib import Path
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

_connection = None


def get_connection():
    """" Singleton to share one connection """
    global _connection
    first_time_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='hosts';"
    if _connection is None:
        _connection = create_connection()
        try:
            cur = _connection.cursor()
            cur.execute(first_time_check)
            rows = cur.fetchall()
            if len(rows) == 0:
                logger.info("No existing host table found in database.")
                setup_tables(_connection)
        except Error as e:
            logger.error("Error scanning for existing database tables: {}".format(e))
            _connection.close()
            raise
    return _connection


def close_connection():
    global _connection
    if _connection is not None:
        try:
            _connection.close()
        except:
            pass


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    logger.info("Opening connection to SQLite at path: {}".format(cur_dir))
    db_file = Path(cur_dir) / "netscanner.db"
    try:
        conn = sqlite3.connect(db_file)
        logger.info("SQLite version: {}".format(sqlite3.version))
        # If needed to debug queries
        # conn.set_trace_callback(print)
    except Error as e:
        logger.error("Error opening SQLite database: {}".format(e))
        conn.close()
        raise
    else:
        return conn


def setup_tables(conn):
    sql = "CREATE TABLE hosts ( \
    id integer PRIMARY KEY, \
    mac text NOT NULL, \
    host_name text, \
    date_added text \
    );"
    try:
        logger.info("Creating database tables for first-time setup.")
        conn.cursor().execute(sql)
        conn.commit()
    except Error as e:
        logger.error("Error creating SQLite table: {}".format(e))
        conn.close()
        raise


def host_exists(mac):
    """" Takes single argument for mac address """
    cur = get_connection().cursor()
    try:
        cur.execute("SELECT id FROM hosts WHERE mac=?", (mac,))
        rows = cur.fetchall()
    except Error as e:
        logger.error("Error fetching records from database: {}".format(e))
        raise
    else:
        if len(rows) == 0:
            logger.info("{} does not appear to be in the database yet".format(mac))
            return False
        else:
            return True


def insert_host(mac, host_name="[none]"):
    """" Takes mac address and host name as arguments """
    cur = get_connection().cursor()
    now = datetime.now()
    try:
        cur.execute("INSERT INTO hosts(mac,host_name,date_added) \
                    VALUES(?,?,?);", (mac, host_name, now.strftime("%d/%m/%Y %H:%M:%S"),))
        get_connection().commit()
        logger.info("Inserted new database record for mac address {}".format(mac))
    except Error as e:
        logger.error("Error inserting records into database: {}".format(e))
        raise
