/*
# tippspiel
# https://github.com/SirCoemgen/tippspiel
# ---------------------------------------
#
#	schema.sql
#	Database layout for the tippspiel.
#
#	Author:  Kevin D. (http://sircoemgen.github.com)
#	Version: 1.0.0 2012-07-02
#	License: WTFPL
*/

/* Structure for users*/
drop table if exists users;
create table users (
	user_id integer primary key autoincrement,
	user_name string not null,
	user_mail string not null,
	user_pass string not null,
	user_score integer,
	user_rank integer,
	user_role integer
);

/* Structure for matches */
drop table if exists matches;
create table matches (
	match_id integer primary key autoincrement,
	match_time integer,
	match_group string not null,
	match_team_home string not null,
	match_team_visitor string not null,
	match_score_home integer,
	match_score_visitor integer
);

/* Structure for bets ('tipp') */
drop table if exists tipps;
create table tipps (
	tipp_id integer primary key autoincrement,
	tipp_time integer,
	tipp_user integer,
	tipp_match integer,
	tipp_score_home integer,
	tipp_score_visitor integer
);

