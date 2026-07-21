{{ config(
    materialized='table'
) }}


select

    vendor_id,

    pickup_datetime,

    dropoff_datetime,

    trip_duration_minutes,

    passenger_count,

    trip_distance,

    fare_amount,

    total_amount


from {{ ref('int_trips') }}