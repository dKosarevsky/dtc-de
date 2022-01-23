select tpep_pickup_datetime::date
from yellow_taxi_trips
where tip_amount = (select max(tip_amount) from yellow_taxi_trips);
