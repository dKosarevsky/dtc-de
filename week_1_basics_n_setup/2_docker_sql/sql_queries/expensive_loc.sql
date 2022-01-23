with trips as (
    select concat(zp."Zone", ' / ', coalesce(zd."Zone", 'Unknown')) as pickup_dropoff_pair,
           avg(total_amount)                                        as avg_price
    from yellow_taxi_trips t
             join zones zp
                  on t."PULocationID" = zp."LocationID"
             join zones zd
                  on t."DOLocationID" = zd."LocationID"
    group by pickup_dropoff_pair
)
select *
from trips
order by avg_price desc
limit 1;
