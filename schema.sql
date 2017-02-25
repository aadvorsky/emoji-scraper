drop table if exists emojis;
create table emojis (
  id integer primary key autoincrement,
  name text not null,
  url text not null
);

drop table if exists categories;
create table categories (
  id integer primary key autoincrement,
  emoji_name text not null,
  category text not null 
);