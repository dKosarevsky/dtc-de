## Week 1 Homework

In this homework we'll prepare the environment 
and practice with terraform and SQL

## Question 1. Google Cloud SDK

Install Google Cloud SDK. What's the version you have? 

To get the version, run `gcloud --version`

```bash
Google Cloud SDK 369.0.0
alpha 2022.01.14
beta 2022.01.14
bq 2.0.72
core 2022.01.14
gsutil 5.6
minikube 1.24.0
skaffold 1.35.1
```

## Google Cloud account 

Create an account in Google Cloud and create a project.


## Question 2. Terraform 

Now install terraform and go to the terraform directory (`week_1_basics_n_setup/1_terraform_gcp/terraform`)

After that, run

* `terraform init`
* `terraform plan`
* `terraform apply` 

Apply the plan and copy the output (after running `apply`) to the form

```bash
var.project
  Your GCP Project ID

  Enter a value: diesel-cat-338820


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west6"
      + project                    = "diesel-cat-338820"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST6"
      + name                        = "dtc_data_lake_diesel-cat-338820"
      + project                     = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_storage_class = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 1s [id=dtc_data_lake_diesel-cat-338820]
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/diesel-cat-338820/datasets/trips_data_all]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

## Prepare Postgres 

Run Postgres and load data as shown in the videos

We'll use the yellow taxi trips from January 2021:

```bash
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

You will also need the dataset with zones:

```bash 
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Download this data and put it to Postgres

## Question 3. Count records 

How many taxi trips were there on January 15?

Consider only trips that started on January 15.

```postgresql
select count(*)
from yellow_taxi_trips
where tpep_pickup_datetime::date = '2021-01-15';
```

```postgresql
53024
```

## Question 4. Largest tip for each day

Find the largest tip for each day. 
On which day it was the largest tip in January?

(note: it's not a typo, it's "tip", not "trip")

```postgresql
select tpep_pickup_datetime::date
from yellow_taxi_trips
where tip_amount = (select max(tip_amount) from yellow_taxi_trips);
```

```postgresql
2021-01-20
```

## Question 5. Most popular destination

What was the most popular destination for passengers picked up 
in central park on January 14?

Enter the zone name (not id). If the zone name is unknown (missing), write "Unknown" 

```postgresql
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
```

```postgresql
Upper East Side South
```

## Question 6. 

What's the pickup-dropoff pair with the largest 
average price for a ride (calculated based on `total_amount`)?

Enter two zone names separated by a slash

For example:

"Jamaica Bay / Clinton East"

If any of the zone names are unknown (missing), write "Unknown". For example, "Unknown / Clinton East". 

```postgresql
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
select pickup_dropoff_pair
from trips
order by avg_price desc
limit 1;
```

```postgresql
Alphabet City / Unknown
```

## Submitting the solutions

* Form for submitting: https://forms.gle/yGQrkgRdVbiFs8Vd7
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 24 January, 17:00 CET

