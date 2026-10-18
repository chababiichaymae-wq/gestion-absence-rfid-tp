from datetime import datetime
from db import db_connect
import socket



def verify_student(num_apogee):

    db = db_connect()
    cursor = db.cursor(dictionary=True)
    if not db:
        return False

    cursor.execute("select * from students where num_apogee = %s;", (num_apogee,))
    student = cursor.fetchone()
    if not student:
        return False

    pc_name = socket.gethostname()

    cursor.execute("select pc_id from pcs where pc_name = %s", (pc_name,))
    pc = cursor.fetchone()

    if not pc:
        cursor.execute("insert into pcs(pc_name) values (%s)", (pc_name,))
        db.commit()
        pc_id = cursor.lastrowid

    pc_id = pc["pc_id"]
    student_id = student["student_id"]

    cursor.execute(
        "Insert into sessions(student_id, pc_id,start_time) values (%s,%s,%s);",
        (student_id,pc_id, datetime.now()))
    db.commit()


    return True