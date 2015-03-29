# Tournament Results

## Create tournament DB and run tests
To run this program you will need to install Vagrant and VirtualBox.

Once that has been installed clone this repository and navigate to the home directory.

The following steps can be used to run the tests for this project:

1. Run command ```vagrant up```

2. Run command ```vagrant ssh```

3. Run command ```python /vagrant/tournament/tournament_test.py```

## File modifications
To attempt extra credit the following changes were made from the provided files

__pg_config.sh__

+ modified to run tournament.sql on start up

__tournament.py__

+ refactored method signatures to be lower case
+ added method delete_player_from_tournament
+ added method delete_tournaments
+ added method count_tournaments
+ added method count_players_in_tournament
+ added method add_new_tournament
+ added method add_player_to_tournament
+ refactored method signature get_player_standings to take in a tournament id
+ added method count_matches_in_tournament
+ added method add_new_match_to_tournament
+ refactored report_match to be report_match_result which takes in a player_id, match_id, and result
+ refactored swiss_pairings to be get_swiss_pairings_for_tournament
+ created helper methods pair_odd_tournament, pair_even_tournament
+ added helper method add_bye
+ added method update_bye_status

__tournament_test.py__

+ refactored tests where signatures had changed
+ refactored tests to accommodate opponent_match_wins, tournaments, odd pairings, and match byes
+ added tests for some of the newly created methods

## Extra Credit
All extra credit was attempted in this project including the following:

+ Odd pairings
+ Opponent Match Wins
+ Match byes
+ Multiple Tournaments

## Project Purpose
This project is a result of Project 2 in the Full Stack Developer course offered by Udacity

