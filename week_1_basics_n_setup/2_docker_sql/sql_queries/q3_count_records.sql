select count(*)
from yellow_taxi_trips
where tpep_pickup_datetime::date = '2021-01-15';
