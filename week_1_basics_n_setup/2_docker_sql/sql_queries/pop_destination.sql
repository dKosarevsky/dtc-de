with trips as (
    select "DOLocationID",
           count(*) as count
    from yellow_taxi_trips t
    where tpep_pickup_datetime::date = '2021-01-14'
      and "PULocationID" = (select "LocationID" from zones where "Zone" = 'Central Park')
    group by "DOLocationID"
)
select "Zone"
from trips
         join zones z
              on trips."DOLocationID" = z."LocationID"
order by count desc
limit 1;
