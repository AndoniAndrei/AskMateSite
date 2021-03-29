from datetime import datetime
import database_common
from flask import render_template, request


def date_and_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# @database_common.connection.handler
# def get_header_from_tables(cursor,table):
#     cursor.execute(f"""SELECT * FROM information_schema.columns WHERE table_name = {table}
#     """)
#     headers = cursor.fetchall()
#     return headers
