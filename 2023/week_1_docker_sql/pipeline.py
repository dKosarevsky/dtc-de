#!/usr/bin/env python
# coding: utf-8

import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = 'green_taxi_data'  # params.table_name

    conn_string = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    print(conn_string)
    engine = create_engine(conn_string)
    connection = engine.connect()

    df_iter = pd.read_csv('green_tripdata_2019-01.csv.gz', compression='gzip', iterator=True, chunksize=100000)
    df = next(df_iter)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while df_iter:
        t_start = time()
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk, took %.3f second' % (t_end - t_start))
    print(f'{table_name} uploaded to {db} database')

    df_zones = pd.read_csv('taxi+_zone_lookup.csv')
    table_name2 = 'taxi_zones'
    df_zones.to_sql(name=table_name2, con=engine, if_exists='replace')
    print(f'{table_name2} uploaded to {db} database')

    connection.invalidate()
    engine.dispose()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    # parser.add_argument('--table_name', help='name of the table where we will write the results to')
    # parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
