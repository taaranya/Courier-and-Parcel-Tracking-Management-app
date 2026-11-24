-- Replace the example tracking number to look up another shipment.
SELECT stamp,status,location FROM movement JOIN parcel ON parcel.id=movement.parcel_id WHERE tracking='DEMO-001' ORDER BY movement.id;
SELECT tracking,destination,status FROM shipment WHERE status IN ('Booked','In Transit','Out for Delivery');
SELECT tracking,destination FROM shipment WHERE status='Delivered';
SELECT tracking,destination FROM shipment WHERE status='Returned';
SELECT c.name,COUNT(s.id) active_parcels FROM courier_staff c LEFT JOIN shipment s ON s.staff=c.id AND s.status NOT IN ('Delivered','Returned') GROUP BY c.id,c.name;
