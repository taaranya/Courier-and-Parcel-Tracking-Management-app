"""Rebuild all figures from the SQLite shipment records."""
import sqlite3
from collections import Counter
from datetime import date
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
with sqlite3.connect((ROOT / "data/courier.db").as_uri()+"?mode=ro",uri=True) as db:
    rows = db.execute("""SELECT booked,due,status,
      (SELECT MAX(stamp) FROM movement WHERE parcel_id=s.id AND status='Delivered')
      FROM shipment s""").fetchall()
months, delays = Counter(), Counter({"On time":0,"1 day late":0,"2+ days late":0})
delivered = 0
for booked,due,status,finished in rows:
    months[date.fromisoformat(booked).strftime("%Y-%m")] += 1
    if status == "Delivered":
        delivered += 1
        late = (date.fromisoformat(finished)-date.fromisoformat(due)).days
        delays["On time" if late<=0 else "1 day late" if late==1 else "2+ days late"] += 1
figures = [("volume","Monthly shipment volume",dict(sorted(months.items())),"Parcels"),
           ("completion","Delivery completion across all bookings",{"Delivered":100*delivered/len(rows),"Other":100*(len(rows)-delivered)/len(rows)} if rows else {},"Percent of bookings"),
           ("delay","Delay among delivered parcels",delays,"Delivered parcels")]
out=ROOT/"analysis/output"
out.mkdir(parents=True,exist_ok=True)
for filename,title,values,unit in figures:
    fig,ax=plt.subplots(figsize=(7,4))
    bars=ax.bar(list(values),list(values.values()),color="#176478",width=.55)
    ax.bar_label(bars,fmt="%.1f" if filename=="completion" else "%d",padding=3)
    ax.set(title=title,ylabel=unit); ax.margins(y=.18)
    if not rows: ax.text(.5,.5,"No bookings",ha="center",transform=ax.transAxes)
    fig.tight_layout();fig.savefig(out/(filename+".png"),dpi=150);plt.close(fig)
print(f"{len(rows)} bookings; {delivered} delivered; {dict(delays)}")
