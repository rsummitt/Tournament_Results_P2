import psycopg2


def get_connection():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def delete_matches():
    """Remove all the match records from the database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM matches''')

    connection.commit()
    connection.close()


def delete_players():
    """Remove all the player records from the database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM players''')

    connection.commit()
    connection.close()


def delete_player_from_tournament(player_id, tournament_id):
    """Deletes a player from the tournament"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM tournament_players WHERE player_id = %s AND tournament_id = %s''',
                   (player_id, tournament_id))

    connection.commit()
    connection.close()


def delete_tournaments():
    """Remove all the tournament records from the database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM tournaments''')

    connection.commit()
    connection.close()


def count_players():
    """Returns the number of players currently registered."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT COALESCE(count(*), 0) AS number_of_players FROM players''')
    result = cursor.fetchone()

    connection.close()

    return result[0]


def count_tournaments():
    """Returns the number of tournaments."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT COALESCE(count(*), 0) AS number_of_tournaments FROM tournaments''')
    result = cursor.fetchone()

    connection.close()

    return result[0]


def count_players_in_tournament(tournament_id):
    """Returns number of players in given tournament."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT COALESCE(count(*), 0) AS number_of_players_in_tournament
                      FROM tournament_players
                      WHERE tournament_id = %s''', (tournament_id,))
    result = cursor.fetchone()

    connection.close()

    return result[0]


def register_player(name):
    """Adds a player to the tournament database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO players (player_name) VALUES (%s) RETURNING player_id''', (name,))
    player_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()
    return player_id


def add_new_tournament(name):
    """Adds a new tournament to the database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO tournaments (tournament_name) VALUES (%s) RETURNING tournament_id''', (name,))
    tournament_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()
    return tournament_id


def add_player_to_tournament(player_id, tournament_id):
    """Adds a player to a tournament."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO tournament_players (player_id, tournament_id)
                      VALUES (%s, %s)''', (player_id, tournament_id))

    connection.commit()
    connection.close()


def get_player_standings(tournament_id):
    """Get standings for specified tournament"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
                    -- Using WITH create a table that contains all players
                    -- omw value

                    WITH player_opponent_wins AS (
                        SELECT p.player_id,

                        -- Add up opponent wins and group by player id

                        (SELECT sum(wins) AS opponent_wins
                        FROM players

                        -- Select all players from players table in below query

                        WHERE player_id IN (

                        -- Select all player ids in below query but leave out player
                        -- so all opponents are returned

                         SELECT player_id
                         FROM match_results
                         WHERE match_id IN (

                         -- Select all matches that involve player and are of specified tournament

                           SELECT mr.match_id
                           FROM match_results mr
                           LEFT JOIN matches m ON m.match_id = mr.match_id
                           WHERE player_id = p.player_id AND m.tournament_id = %s) AND player_id != p.player_id)) AS omw
                        FROM players p
                        GROUP BY p.player_id)

                    SELECT p.player_id,
                           p.player_name,
                           p.wins,
                           p.losses,
                           p.draws,
                           COALESCE(count(mr.*), 0) AS num_matches,
                           p.received_bye
                    FROM players p
                    LEFT JOIN player_opponent_wins po ON p.player_id = po.player_id -- used to get omw
                    LEFT JOIN tournament_players tp ON p.player_id = tp.player_id -- used to get correct tournament
                    LEFT JOIN match_results mr ON p.player_id = mr.player_id -- used to get correct match results
                    LEFT JOIN matches m ON mr.match_id = m.match_id -- chained to get correct matches
                    WHERE tp.tournament_id = %s -- Specify tournament
                    GROUP BY p.player_id , po.omw
                    ORDER BY p.wins DESC , po.omw DESC''', (tournament_id, tournament_id))

    standings = [(row[0], str(row[1]), row[2], row[3], row[4], int(row[5]), row[6]) for row in cursor.fetchall()]

    connection.close()
    return standings


def count_matches_in_tournament(tournament_id):
    """Get number of matches in a tournament"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT COALESCE(count(m.match_id), 0) AS num_tournament_matches
                      FROM matches m
                      WHERE tournament_id = %s''', (tournament_id,))
    result = cursor.fetchone()

    connection.close()
    return result[0]


def add_new_match_to_tournament(tournament_id):
    """Add a new match to a tournament"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO matches (tournament_id)
                      VALUES (%s) RETURNING match_id''', (tournament_id,))
    result = cursor.fetchone()[0]

    connection.commit()
    connection.close()
    return result


def report_match_result(player_id, match_id, result):
    """Record a players result in a specific match"""
    if result not in ("win", "loss", "draw"):
        raise ValueError("Invalid result entered")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO match_results (player_id, match_id, result)
                      VALUES (%s, %s, %s)''', (player_id, match_id, result))

    if result == "win":
        cursor.execute('''UPDATE players SET wins = wins + 1 WHERE player_id = %s''', (player_id,))
    elif result == "loss":
        cursor.execute('''UPDATE players SET losses = losses + 1 WHERE player_id = %s''', (player_id,))
    elif result == "draw":
        cursor.execute('''UPDATE players SET draws = draws + 1 WHERE player_id = %s''', (player_id,))
    else:
        raise ValueError("There was a problem updating a players record.")

    connection.commit()
    connection.close()


def get_swiss_pairings_for_tournament(tournament_id):
    """Return a list of pairs of players for the next round of a match"""
    pairings = []
    standings = get_player_standings(tournament_id)
    standings.reverse()

    if len(standings) % 2 != 0:
        pair_odd_tournament(standings, pairings)
    else:
        pair_even_tournament(standings, pairings)

    return pairings


def pair_odd_tournament(standings, pairings):
    """ Returns pairings for Odd numbered tournament based on tournament standings"""
    previous = None
    bye_not_assigned = True

    while len(standings) != 0:

        current = standings.pop()

        # Assign a bye to a user that has not had one
        if not current[4] and bye_not_assigned:
            add_bye(current, pairings)
            # Set the flag to ensure we do not assign a bye to anybody else this round
            bye_not_assigned = False
            # Move on to next user
            continue

        # Match previous and current players
        if previous:
            pairings.append((previous[0], previous[1], current[0], current[1]))
        else:  # If we are iterating on first player in standings set current to previous
            previous = current
            continue


def pair_even_tournament(standings, pairings):
    """ Returns pairings for Even numbered tournament based on tournament standings"""
    while len(standings) != 0:
        player_one = standings.pop()
        player_two = standings.pop()
        pairings.append((player_one[0], player_one[1], player_two[0], player_two[1]))


def add_bye(player, pairings):
    """ Pairs a player with a BYE in pairings list"""
    pairings.append((player[0], player[1], None, "BYE"))
    update_bye_status(player)


def update_bye_status(bye_recipient):
    """ Updates player record to indicate he/she has received a bye"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE players SET received_bye = TRUE WHERE player_id = %s''',
                   (bye_recipient[0],))

    connection.commit()
    connection.close()



