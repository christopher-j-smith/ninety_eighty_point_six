create view game_fact as 
select gh.game_id
	,  gh.first_player
	,  gh.second_player
	,  gr.last_player
	,  gh.first_column_played
	,  gr.game_result
from(select gh.game_id 
		 ,  max(case when gh.move_number = 1 then gh.player_id end) as first_player
		 ,  max(case when gh.move_number = 2 then gh.player_id end) as second_player
		 ,  max(case when gh.move_number = 1 then gh.column end)    as first_column_played
     from game_history as gh
     group by game_id) as gh
inner join(select game_id
		  		, "result" as game_result
		  		, max(player_id) as last_player
		   from game_history
		   where result is not null
		   group by game_id
		  		  , "result") as gr on gh.game_id = gr.game_id; 
create view column_win_ratios as 
select sum(case when first_column_played = 1 then 1 else 0 end)          as first_column_wins
	,  sum(case when first_column_played = 1 then 1 else 0 end) / sum(1.00) as first_column_wins_ratio
	,  sum(case when first_column_played = 2 then 1 else 0 end)          as second_column_wins
	,  sum(case when first_column_played = 2 then 1 else 0 end) / sum(1.00) as second_column_wins_ratio
	,  sum(case when first_column_played = 3 then 1 else 0 end)          as third_column_wins
	,  sum(case when first_column_played = 3 then 1 else 0 end) / sum(1.00) as third_column_wins_ratio
	,  sum(case when first_column_played = 4 then 1 else 0 end)          as fourth_column_wins
	,  sum(case when first_column_played = 3 then 1 else 0 end) / sum(1.00) as fourth_column_wins_ratio
	,  sum(1) as total_wins
from game_fact
where game_result = 'win';
create view nationality_play_totals as 
select player_dim.nationality
	,  count(distinct game_id) as number_of_games_unique_nationalities
	,  count(game_id)          as number_of_games
from game_fact 
inner join player_dim on game_fact.first_player  = player_dim.id
					  or game_fact.second_player = player_dim.id
group by player_dim.nationality;
create view player_fact as
select player_id
	,  count(player_games.game_id) as number_of_games
	,  sum(case when player_games.player_id = game_fact.last_player
		   		 and game_fact.game_result = 'win' then 1 else 0 end) as wins
	,  sum(case when player_games.player_id != game_fact.last_player
		   		 and game_fact.game_result = 'win' then 1 else 0 end) as losses
    ,  sum(case when game_fact.game_result = 'draw' then 1 else 0 end) as draws
from(select player_id
	,  game_id
	from game_history
	group by player_id
	 		,game_id) as player_games
inner join game_fact on player_games.game_id = game_fact.game_id
group by player_id;
select * from column_win_ratios;
select * from nationality_play_totals;
select player_dim.first_name
	,  player_dim.last_name
	,  player_dim.email
	,  case when player_fact.wins = 1 then 'winner'
			when player_fact.losses = 1 then 'loser'
			when player_fact.draws = 1 then 'draw'
			else 'error' end as customization_flag
from player_fact 
inner join player_dim on player_fact.player_id = player_dim.id
where player_fact.number_of_games = 1
