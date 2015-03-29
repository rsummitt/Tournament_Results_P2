from tournament import *


def test_delete_matches():
    delete_matches()
    print "1. Old matches can be deleted."


def test_delete():
    delete_tournaments()
    delete_matches()
    delete_players()
    print "2. Player records can be deleted."


def test_registered_player_count():
    delete_tournaments()
    delete_matches()
    delete_players()
    c = count_players()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def test_register():
    delete_tournaments()
    delete_matches()
    delete_players()
    register_player("Chandra Nalaar")
    c = count_players()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def test_register_count_delete():
    delete_tournaments()
    delete_matches()
    delete_players()
    register_player("Markov Chaney")
    register_player("Joe Malik")
    register_player("Mao Tsu-hsi")
    register_player("Atlanta Hope")
    c = count_players()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    delete_players()
    c = count_players()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def test_add_new_tournament():
    delete_tournaments()
    delete_players()
    add_new_tournament("Test Tournament")
    t = count_tournaments()
    if t != 1:
        raise ValueError("After adding a tournament, count_tournament should return one.")
    print "6. Tournaments can be added."


def test_add_player_to_tournament():
    delete_tournaments()
    delete_players()
    new_player = register_player("Markov Chaney")
    new_tournament = add_new_tournament("Test Tournament")
    add_player_to_tournament(new_player, new_tournament)
    tp = count_players_in_tournament(new_tournament)
    if tp != 1:
        raise ValueError("After adding player to tournament, count_players_in_tournament should return one.")
    print "7. Players can be added to a tournament."


def test_delete_player_from_tournament():
    delete_tournaments()
    delete_players()
    new_player = register_player("Markov Chaney")
    new_tournament = add_new_tournament("Test Tournament")
    add_player_to_tournament(new_player, new_tournament)
    delete_player_from_tournament(new_player, new_tournament)
    tp = count_players_in_tournament(new_tournament)
    if tp != 0:
        raise ValueError("After deleting player from tournament, count_players_in_tournament should return zero.")
    print "8. Players can be removed from tournament"


def test_add_a_match_to_a_tournament():
    delete_tournaments()
    delete_players()
    new_tournament = add_new_tournament("Test Tournament")
    add_new_match_to_tournament(new_tournament)
    tm = count_matches_in_tournament(new_tournament)
    if tm != 1:
        raise ValueError("After adding a match to a tournament, count_matches_in_tournament should return one.")
    print "9. Matches can be added to a tournament."


def test_standings_before_match():
    delete_tournaments()
    delete_players()
    player_one = register_player("Melpomene Murray")
    player_two = register_player("Randy Schwartz")
    player_three = register_player("Bill Brasky")
    tournament_one = add_new_tournament("Tournament One")
    tournament_two = add_new_tournament("Tournament Two")
    add_player_to_tournament(player_one, tournament_one)
    add_player_to_tournament(player_two, tournament_one)
    add_player_to_tournament(player_three, tournament_two)

    standings = get_player_standings(tournament_one)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 7:
        raise ValueError("Each playerStandings row should have 7 columns.")
    [(id1, name1, wins1, losses1, draws1, matches1, bye1),
     (id2, name2, wins2, losses2, draws2, matches2, bye2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if {name1, name2} != {"Melpomene Murray", "Randy Schwartz"}:
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "10. Newly registered players appear in the standings with no matches."


def test_report_match_result():
    delete_tournaments()
    delete_players()

    new_tournament = add_new_tournament("Tournament")

    new_match_one = add_new_match_to_tournament(new_tournament)
    new_match_two = add_new_match_to_tournament(new_tournament)

    player_one = register_player("Bruno Walton")
    player_two = register_player("Boots O'Neal")
    player_three = register_player("Cathy Burton")
    player_four = register_player("Diane Grant")

    add_player_to_tournament(player_one, new_tournament)
    add_player_to_tournament(player_two, new_tournament)
    add_player_to_tournament(player_three, new_tournament)
    add_player_to_tournament(player_four, new_tournament)

    report_match_result(player_one, new_match_one, "win")
    report_match_result(player_two, new_match_one, "loss")
    report_match_result(player_three, new_match_two, "win")
    report_match_result(player_four, new_match_two, "loss")
    standings = get_player_standings(new_tournament)
    for (i, n, w, l, d, m, b) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (player_one, player_three) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (player_two, player_four) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "11. After a match, players have updated standings."


def test_pairings_for_tournament():
    delete_tournaments()
    delete_players()

    new_tournament = add_new_tournament("Tournament")

    new_match_one = add_new_match_to_tournament(new_tournament)
    new_match_two = add_new_match_to_tournament(new_tournament)

    player_one = register_player("Bruno Walton")
    player_two = register_player("Boots O'Neal")
    player_three = register_player("Cathy Burton")
    player_four = register_player("Diane Grant")

    add_player_to_tournament(player_one, new_tournament)
    add_player_to_tournament(player_two, new_tournament)
    add_player_to_tournament(player_three, new_tournament)
    add_player_to_tournament(player_four, new_tournament)

    report_match_result(player_one, new_match_one, "win")
    report_match_result(player_two, new_match_one, "loss")
    report_match_result(player_three, new_match_two, "win")
    report_match_result(player_four, new_match_two, "loss")

    pairings = get_swiss_pairings_for_tournament(new_tournament)
    [(pid1, player_name_one, pid2, player_name_two), (pid3, player_name_three, pid4, player_name_four)] = pairings
    correct_pairs = {frozenset([player_one, player_three]), frozenset([player_two, player_four])}
    actual_pairs = {frozenset([pid1, pid2]), frozenset([pid3, pid4])}
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "12. After one match, players with one win are paired."


def test_bye_allocation():
    delete_tournaments()
    delete_players()

    new_tournament = add_new_tournament("Tournament")

    new_match_one = add_new_match_to_tournament(new_tournament)

    player_one = register_player("Bruno Walton")
    player_two = register_player("Boots O'Neal")
    player_three = register_player("Cathy Burton")

    add_player_to_tournament(player_one, new_tournament)
    add_player_to_tournament(player_two, new_tournament)
    add_player_to_tournament(player_three, new_tournament)

    report_match_result(player_one, new_match_one, "win")
    report_match_result(player_two, new_match_one, "loss")

    pairings = get_swiss_pairings_for_tournament(new_tournament)
    [(pid1, player_name_one, pid2, player_name_two), (pid3, player_name_three, pid4, player_name_four)] = pairings
    correct_pairs = {frozenset([player_one, None]), frozenset([player_two, player_three])}
    actual_pairs = {frozenset([pid1, pid2]), frozenset([pid3, pid4])}
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match in odd pairing, one player should have a bye and the others are paired")

    standings = get_player_standings(new_tournament)
    for (i, n, w, l, d, m, b) in standings:
        if i in (player_one,) and True != b:
            raise ValueError("Player one should have received a bye")
    print "13. After one match, player with a win receives a bye and other two players are paired."


def test_report_draw():
    delete_tournaments()
    delete_players()

    new_tournament = add_new_tournament("Tournament")

    new_match_one = add_new_match_to_tournament(new_tournament)

    player_one = register_player("Bruno Walton")
    player_two = register_player("Boots O'Neal")

    add_player_to_tournament(player_one, new_tournament)
    add_player_to_tournament(player_two, new_tournament)

    report_match_result(player_one, new_match_one, "draw")
    report_match_result(player_two, new_match_one, "draw")

    standings = get_player_standings(new_tournament)
    for (i, n, w, l, d, m, b) in standings:
        if i in (player_one, player_two) and d != 1:
            raise ValueError("Each match winner should have one draw recorded.")
    print "14. After a draw, both players have a draw in their record."


if __name__ == '__main__':
    test_delete_matches()
    test_delete()
    test_registered_player_count()
    test_register()
    test_register_count_delete()
    test_add_new_tournament()
    test_add_player_to_tournament()
    test_delete_player_from_tournament()
    test_add_a_match_to_a_tournament()
    test_standings_before_match()
    test_report_match_result()
    test_pairings_for_tournament()
    test_bye_allocation()
    test_report_draw()
    print "Success! All tests pass!"