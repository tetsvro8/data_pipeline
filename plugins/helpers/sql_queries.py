class SqlQueries:
    create_artists_table = """
    DROP TABLE IF EXISTS public.artists;
    CREATE TABLE public.artists (
	    artistid varchar(1024) NOT NULL,
	    name varchar(1024),
	    location varchar(1024),
	    lattitude numeric(18,0),
	    longitude numeric(18,0)
    );
    """
    create_songplays_table = """
    DROP TABLE IF EXISTS public.songplays;
    CREATE TABLE public.songplays (
	    playid varchar(32) NOT NULL,
	    start_time timestamp NOT NULL,
	    userid int4 NOT NULL,
	    "level" varchar(1024),
	    songid varchar(1024),
	    artistid varchar(1024),
	    sessionid int4,
	    location varchar(1024),
	    user_agent varchar(1024),
	    CONSTRAINT songplays_pkey PRIMARY KEY (playid)
    );
    """

    create_songs_table = """
    DROP TABLE IF EXISTS public.songs;
    CREATE TABLE public.songs (
	    songid varchar(1024) NOT NULL,
	    title varchar(1024),
	    artistid varchar(1024),
	    "year" int4,
	    duration numeric(18,0),
	    CONSTRAINT songs_pkey PRIMARY KEY (songid)
    );
    """
    create_staging_events_table = """
    DROP TABLE IF EXISTS public.staging_events;
    CREATE TABLE public.staging_events (
	    artist varchar(1024),
	    auth varchar(1024),
	    firstname varchar(1024),
	    gender varchar(1024),
	    iteminsession int4,
	    lastname varchar(1024),
	    length numeric(18,0),
	    "level" varchar(1024),
	    location varchar(1024),
	    "method" varchar(1024),
	    page varchar(1024),
	    registration numeric(18,0),
	    sessionid int4,
	    song varchar(1024),
	    status int4,
	    ts int8,
	    useragent varchar(1024),
	    userid int4
    );
    """

    create_staging_songs_table = """
    DROP TABLE IF EXISTS public.staging_songs;
    CREATE TABLE public.staging_songs (
	    num_songs int4,
	    artist_id varchar(1024),
	    artist_name varchar(1024),
	    artist_latitude numeric(18,0),
	    artist_longitude numeric(18,0),
	    artist_location varchar(1024),
	    song_id varchar(1024),
	    title varchar(1024),
	    duration numeric(18,0),
	    "year" int4
    );
    """

    create_time_table = """
    DROP TABLE IF EXISTS public."time";
    CREATE TABLE public."time" (
	    start_time timestamp NOT NULL,
	    "hour" int4,
	    "day" int4,
	    week int4,
	    "month" varchar(1024),
	    "year" int4,
	    weekday varchar(1024),
	    CONSTRAINT time_pkey PRIMARY KEY (start_time)
    ) ;
    """

    create_users_table = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE public.users (
	    userid int4 NOT NULL,
	    first_name varchar(1024),
	    last_name varchar(1024),
	    gender varchar(1024),
	    "level" varchar(1024),
	    CONSTRAINT users_pkey PRIMARY KEY (userid)
    );
    """

    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)