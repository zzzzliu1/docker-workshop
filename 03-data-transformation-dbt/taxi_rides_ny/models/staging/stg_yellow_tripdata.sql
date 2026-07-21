{{ config(
    materialized='view'
) }}


select

    -- identifiers
    VendorID as vendor_id,

    -- timestamps
    SAFE_CAST(
    tpep_pickup_datetime AS TIMESTAMP
    ) AS pickup_datetime,


    SAFE_CAST(
    tpep_dropoff_datetime AS TIMESTAMP
    ) AS dropoff_datetime,


    -- trip information
    passenger_count,

    trip_distance,

    RatecodeID as rate_code_id,

    store_and_fwd_flag,

    PULocationID as pickup_location_id,

    DOLocationID as dropoff_location_id,


    -- payment
    cast(payment_type as integer) as payment_type,

    fare_amount,

    tip_amount,

    tolls_amount,

    total_amount


from {{ source('raw','yellow_tripdata') }}

where
 VendorID is not null
 and payment_type is not null