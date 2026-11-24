"""SQLite operations called by the Java console. Run from the project folder."""
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = os.environ.get("COURIER_DB", str(ROOT / "data" / "courier.db"))
REPORTS = (ROOT / "sql/reports.sql").read_text().split(";")
TODAY = date.today().isoformat()


def display(cursor):
    print(" | ".join(column[0] for column in cursor.description))
    rows = cursor.fetchall()
    for row in rows:
        print(" | ".join(str(value) for value in row))
    if not rows:
        print("(no records)")


def execute(db, op, args):
    if op == "customer":
        row = db.execute("INSERT INTO customer(name,phone,address) VALUES(?,?,?)", args)
        print("Customer ID:", row.lastrowid)
    elif op == "staff":
        row = db.execute("INSERT INTO courier_staff(name) VALUES(?)", args)
        print("Staff ID:", row.lastrowid)
    elif op == "list":
        display(db.execute("SELECT * FROM customer"))
        display(db.execute("SELECT * FROM courier_staff"))
        display(db.execute("SELECT tracking,status,charge FROM shipment"))
    elif op == "book":
        row = db.execute("INSERT INTO parcel(tracking,sender,receiver,kind,kg,destination,zone,service,booked,due,charge) VALUES(?,?,?,?,?,?,?,?,?,?,?)", args)
        db.execute("INSERT INTO movement(parcel_id,stamp,status,location) VALUES(?,?,'Booked','Booking office')", (row.lastrowid,TODAY))
        print("Booked", args[0], "| INR", args[-1], "| Due", args[-2])
    elif op == "report":
        for query in REPORTS[1:5]:
            display(db.execute(query))
    else:
        row = db.execute("SELECT id,status,staff FROM shipment WHERE tracking=?", (args[0],)).fetchone()
        if row is None:
            raise ValueError("Unknown tracking number.")
        pid,status,staff = row
        if op == "history":
            display(db.execute("SELECT stamp,status,location FROM movement WHERE parcel_id=? ORDER BY id",(pid,)))
            display(db.execute("SELECT stamp,outcome,reason FROM attempt WHERE parcel_id=? ORDER BY id",(pid,)))
            return
        if status in ("Delivered","Returned"):
            raise ValueError("Shipment is closed.")
        if op == "assign":
            db.execute("INSERT INTO assignment(parcel_id,staff_id,assigned) VALUES(?,?,?)",(pid,args[1],TODAY))
        elif op == "move":
            new,location = args[1:]
            allowed = {"Booked":["In Transit","Returned"],"In Transit":["In Transit","Out for Delivery","Returned"],"Out for Delivery":["Returned"]}
            if new not in allowed[status] or (new=="Out for Delivery" and staff is None):
                raise ValueError("Invalid movement or missing delivery assignment.")
            db.execute("INSERT INTO movement(parcel_id,stamp,status,location) VALUES(?,?,?,?)",(pid,TODAY,new,location))
        elif op == "attempt":
            if status != "Out for Delivery" or staff is None:
                raise ValueError("Assign and dispatch this parcel first.")
            outcome,reason,location=args[1:]
            db.execute("INSERT INTO attempt(parcel_id,stamp,outcome,reason) VALUES(?,?,?,?)",(pid,TODAY,outcome,reason))
            if outcome=="Delivered":
                db.execute("INSERT INTO movement(parcel_id,stamp,status,location) VALUES(?,?,'Delivered',?)",(pid,TODAY,location))
        else:
            raise ValueError("Unknown operation.")
        print("Saved.")


if __name__ == "__main__":
    try:
        Path(DB).parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(DB) as db:
            db.executescript((ROOT / "sql/schema.sql").read_text())
            db.execute("BEGIN IMMEDIATE")
            execute(db,sys.argv[1],sys.argv[2:])
    except (ValueError,sqlite3.Error) as error:
        print("Rejected:",error)
        sys.exit(1)
