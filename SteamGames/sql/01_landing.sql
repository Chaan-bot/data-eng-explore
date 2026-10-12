-- Landing layer: mirrors the source files as closely as possible.
-- Every column is text; no constraints, no casts, no cleverness. The job of
-- this layer is to accept the file without argument. Typing happens in 02.
--
-- Safe to re-run: drops and recreates.

create schema if not exists raw;

drop table if exists raw.games_csv;
create table raw.games_csv (
  appid                      text,
  name                       text,
  release_date               text,
  estimated_owners           text,
  peak_ccu                   text,
  required_age               text,
  price                      text,
  discount                   text,   -- header defect: see ingest.py
  dlc_count                  text,   -- header defect: see ingest.py
  about_the_game             text,
  supported_languages        text,
  full_audio_languages       text,
  reviews                    text,
  header_image               text,
  website                    text,
  support_url                text,
  support_email              text,
  windows                    text,
  mac                        text,
  linux                      text,
  metacritic_score           text,
  metacritic_url             text,
  user_score                 text,
  positive                   text,
  negative                   text,
  score_rank                 text,
  achievements               text,
  recommendations            text,
  notes                      text,
  average_playtime_forever   text,
  average_playtime_two_weeks text,
  median_playtime_forever    text,
  median_playtime_two_weeks  text,
  developers                 text,
  publishers                 text,
  categories                 text,
  genres                     text,
  tags                       text,
  screenshots                text,
  movies                     text    -- always empty in this dataset
);

drop table if exists raw.games_json;
create table raw.games_json (
  appid text,
  data  jsonb
);

comment on table raw.games_csv  is 'games.csv as shipped, header defect repaired by ingest.py. All text.';
comment on table raw.games_json is 'games.json, one JSONB document per appid.';