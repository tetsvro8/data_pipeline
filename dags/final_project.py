from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from operators import (StageToRedshiftOperator, LoadFactOperator,
                       LoadDimensionOperator, DataQualityOperator, CreateTablesOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': pendulum.now(),
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *',
    catchup = False,
    max_active_runs=1
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    create_tables = CreateTablesOperator(
        task_id='Create_tables',
        sql_lists = [
            SqlQueries.create_artists_table,
            SqlQueries.create_songplays_table,
            SqlQueries.create_songs_table,
            SqlQueries.create_staging_events_table,
            SqlQueries.create_staging_songs_table,
            SqlQueries.create_time_table,
            SqlQueries.create_users_table
        ]
    )

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table = 'staging_events',
        s3_key = 'log-data',
        json_paths = 's3://igutetsu/log_json_path.json'
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table = 'staging_songs',
        s3_key = 'song-data',
        json_paths = 'auto'
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        table = 'songplays',
        select_sql = SqlQueries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        table = 'users',
        select_sql = SqlQueries.user_table_insert,
        truncate_table = True
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        table = 'songs',
        select_sql = SqlQueries.song_table_insert,
        truncate_table = True
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        table = 'artists',
        select_sql = SqlQueries.artist_table_insert,
        truncate_table = True
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        table = 'time',
        select_sql = SqlQueries.time_table_insert,
        truncate_table = True
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        tables=[
            'songplays',
            'users',
            'songs',
            'artists',
            'time'
        ]
    )

    finish_operator = DummyOperator(task_id='Stop_execution')

    start_operator >> create_tables

    create_tables >> stage_events_to_redshift
    create_tables >> stage_songs_to_redshift

    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table

    load_songplays_table >> [load_artist_dimension_table, load_song_dimension_table, load_time_dimension_table, load_user_dimension_table]

    [load_artist_dimension_table, load_song_dimension_table, load_time_dimension_table, load_user_dimension_table] >> run_quality_checks

    run_quality_checks >> finish_operator

final_project_dag = final_project()