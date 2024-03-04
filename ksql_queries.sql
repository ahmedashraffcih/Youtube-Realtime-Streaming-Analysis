-- Creating stream
CREATE STREAM youtube_videos (
   video_id VARCHAR KEY,
   title VARCHAR,
   likes INTEGER,
   comments INTEGER,
   views INTEGER,
   favorites INTEGER,
   thumbnails VARCHAR
) WITH (
  KAFKA_TOPIC = 'youtube_videos',
  PARTITIONS = 1,
  VALUE_FORMAT = 'JSON'
);

-- SELECT queries
SELECT
VIDEO_ID,
latest_by_offset(title,2) as title,
latest_by_offset(comments,2)[1] as comments_previous,
latest_by_offset(comments,2)[2] as comments_current,
latest_by_offset(likes,2)[1] as likes_previous,
latest_by_offset(likes,2)[2] as likes_current,
latest_by_offset(views,2)[1] as views_previous,
latest_by_offset(views,2)[2] as views_current,
latest_by_offset(favorites,2)[1] as favorites_previous,
latest_by_offset(favorites,2)[2] as favorites_current
FROM youtube_videos
GROUP BY VIDEO_ID
EMIT CHANGES;

-- Create table to find when the changes happened
CREATE TABLE youtube_track_changes WITH(KAFKA_TOPIC = 'youtube_track_changes') AS
SELECT
VIDEO_ID,
latest_by_offset(title) as title,
latest_by_offset(comments,2)[1] as comments_previous,
latest_by_offset(comments,2)[2] as comments_current,
latest_by_offset(likes,2)[1] as likes_previous,
latest_by_offset(likes,2)[2] as likes_current,
latest_by_offset(views,2)[1] as views_previous,
latest_by_offset(views,2)[2] as views_current,
latest_by_offset(favorites,2)[1] as favorites_previous,
latest_by_offset(favorites,2)[2] as favorites_current
FROM youtube_videos
GROUP BY VIDEO_ID;

-- select only videos with likes changes
SELECT * FROM youtube_track_changes
WHERE likes_previous <> likes_current
EMIT CHANGES;

-- Create Strem for telegram bot notifications
CREATE STREAM telegram_notify(
  `chat_id` VARCHAR,
  `text` VARCHAR
) WITH (
  KAFKA_TOPIC = 'telegram_notify',
  PARTITIONS = 1,
  VALUE_FORMAT = 'avro'
);

-- Testing Telegram
insert into TELEGRAM_NOTIFY VALUES ('926030214','Testing Message');
insert into TELEGRAM_NOTIFY VALUES ('926030214','Can you see this?');

-- Create stream for getting values send to telegram topic
CREATE STREAM youtube_track_changes_stream (
   title VARCHAR,
   likes_previous INTEGER,
   likes_current INTEGER,
   comments_previous INTEGER,
   comments_current INTEGER,
   views_previous INTEGER,
   views_current INTEGER,
   favorites_previous INTEGER,
   favorites_current INTEGER,
   thumbnails VARCHAR
) WITH (
  KAFKA_TOPIC = 'youtube_videos',
  PARTITIONS = 1,
  VALUE_FORMAT = 'JSON'
);

-- Inserting into telegram topic the new updates
SELECT '926030214' `chat_id`,
concat('Likes Changed: ',
      title,
      '-',
      cast(likes_previous as string),
      ': ',
      cast(likes_current as string)) as `Text`
FROM youtube_track_changes
WHERE likes_previous <> likes_current;