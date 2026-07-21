{{ config(
    materialized='table'
) }}


select

    date(pickup_datetime) as pickup_date,


    count(*) as total_trips,


    avg(trip_distance) as avg_trip_distance,


    avg(trip_duration_minutes) as avg_trip_duration_minutes,


    sum(total_amount) as total_revenue,


    avg(total_amount) as avg_fare


from {{ ref('fact_trips') }}


group by 1