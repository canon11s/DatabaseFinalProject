drop schema if exists soccer;
create database soccer;
use soccer;


drop table if exists league;
create table league (
	league_id int primary key auto_increment,
    name varchar(25) not null,
    country varchar(25) not null,
    tier int not null
);

insert into league (league_id, name, country, tier) values
(1, 'Premier League', "England", 1),
(2, 'La Liga', 'Spain', 1),
(3, 'Championship', 'England', 2),
(4, 'Serie A', 'Italy', 1),
(5, 'Serie B', 'Italy', 2);

drop table if exists club;
create table club (
	club_id int primary key auto_increment,
    name varchar(25) not null,
    league_id int not null,
    foreign key(league_id) references league(league_id)
);

insert into club (club_id, name, league_id) values
(1, 'AFC Bournemouth', 1),
(2, 'Arsenal', 1),
(3, 'Brighton and Hove Albion', 1),
(4, 'Burnley', 1),
(5, 'Cardiff City', 1),
(6, 'Chelsea', 1),
(7, 'Crystal Palace', 1),
(8, 'Everton', 1),
(9, 'Fulham', 1),
(10, 'Huddersfield Town', 1),
(11, 'Leicester City', 1),
(12, 'Liverpool', 1),
(13, 'Manchester City', 1),
(14, 'Mancehster United', 1),
(15, 'Newcastle United', 1),
(16, 'Southampton', 1),
(17, 'Tottenham Hotspur', 1),
(18, 'Watford', 1),
(19, 'West Ham United', 1),
(20, 'Wolverhampton Wanderers', 1);

drop table if exists player;
create table player (
	player_id int primary key auto_increment,
    name varchar(100) not null,
    club_id int not null,
    foreign key(club_id) references club(club_id),
    position enum('F', 'M', 'D'),
    status enum('FA', 'WW', 'OWNED'),
    game_played int not null,
    goal int not null,
    assist int not null,
    key_pass int not null,
    fantasy_assist int not null,
    shot_on_target int not null,
    tackle int not null,
    disposession int not null,
    foul_suffered int not null,
    yellow_card int not null,
    second_yellow_card int not null,
    red_card int not null,
    accurate_cross int not null,
    interception int not null,
    clearance int not null,
    aerial_won int not null,
    own_goal int not null,
    goal_against_defender int not null,
    clean_sheet int not null
);

select * from player;

insert into player (player_id, name, goals, assists, position, club_id) values
(1, 'luke', 3, 0, 'For', 1),
(2, 'canon', 5, 1, 'Mid', 1),
(3, 'collin', 7, 2, 'Def', 1),
(4, 'isaak', 1, 3, 'Def', 1);


drop table if exists player_award;
create table player_award (
	award_id int primary key auto_increment,
    name varchar(45) not null,
    player_id int not null,
    foreign key(player_id) references player(player_id)
);

insert into player_award (award_id, name, player_id) values
(1, 'Biggest Loser Award', 1);

drop table if exists manager;
create table manager (
	manager_id int primary key auto_increment,
    name varchar(45) not null,
    club_id int not null,
    foreign key(club_id) references club(club_id)
);

insert into manager (manager_id, name, club_id) values
(1, 'MrBitchBoy', 1);

drop table if exists manager_award;
create table manager_award (
	award_id int primary key auto_increment,
    name varchar(45) not null,
    manager_id int not null,
    foreign key(manager_id) references manager(manager_id)
);

insert into manager_award (award_id, name, manager_id) values
(1, 'Worst Manager Ever Bitch', 1);
