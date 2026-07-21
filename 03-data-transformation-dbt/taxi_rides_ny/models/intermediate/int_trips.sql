{{ config(
    materialized='view'
) }}

select

    vendor_id,

    pickup_datetime,

    dropoff_datetime,

    passenger_count,

    trip_distance,

    fare_amount,

    total_amount,

    timestamp_diff(
        dropoff_datetime,
        pickup_datetime,
        minute
    ) as trip_duration_minutes


from {{ ref('stg_yellow_tripdata') }}