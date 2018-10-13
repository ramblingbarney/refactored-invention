import file_operations
import json
from collections import OrderedDict
from itertools import islice
from operator import itemgetter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# this is a python implenentation of the published theory
# https://en.wikipedia.org/wiki/Levenshtein_distance
# I have used a library provided by SeatGeek
# https://github.com/seatgeek/fuzzywuzzy


'''levenshtein string comparison'''
levenshtein_score = (
    lambda to_be_scored_string, answer: fuzz.ratio(to_be_scored_string, answer)
    )


def create_list_all_players_names(all_game_players):
    '''create a list of all players names'''

    names_dict = {}
    names = list(all_game_players.values())

    for name in names:
        name_array = name.split(",")
        # add to a dictionary by player name as key and score as value
        names_dict[name_array[0]] = int(name_array[1])

    # sort names dictionary by value
    sorted_names_dict = sorted(
        names_dict.items(), key=itemgetter(1), reverse=True)

    ordered_player_names = list(OrderedDict(sorted_names_dict).keys())

    return ordered_player_names


def create_list_all_players_names_logged_in(all_game_players):
    '''create a list of all players names that are logged in'''

    names_dict = {}
    ordered_logged_in_player_names = []
    names = list(all_game_players.values())

    for name in names:
        name_array = name.split(",")
        # add to a dictionary by player name as key and score as value
        names_dict[name_array[0]] = int(name_array[2])

    for key, value in names_dict.items():
        if (value == 1):
            ordered_logged_in_player_names.append(key)

    return ordered_logged_in_player_names


def create_song_list_each_name(names):
    '''create a list of songs and scores per name'''

    name_songs_with_scores = {}
    users_history = OrderedDict()

    for name in names:
        name_individual_songs = []
        # select all songs by person, if no songs 'None' is returned
        # 'first' returns the first result, 'all' returns all results
        raw_result = file_operations.search_from_file(
                    'data/song_scores.txt', name, 1)

        if (raw_result is not None):
            for key, value in raw_result.items():
                name_individual_songs.append(
                    "{0} - {1}".format(
                        value.split(",")[1], value.split(",")[2]))
        else:
            name_individual_songs.append('No Completed Song Scores')

        users_history[name] = name_individual_songs

    return users_history


def generate_leaderboard(leaderboard_length):
    '''create a leaderboard of n length'''

    # select all player naames
    all_players = file_operations.read_from_file('data/players.txt')
    # create a list of player names ordered by total score desceding
    names_in_order = create_list_all_players_names(all_players)
    # create a list of each players songs in the same order as 'names_in_order'
    songs_scores_per_player_order = create_song_list_each_name(names_in_order)

    if (len(list(all_players.values())) == 0):
        # return placeholders if no players
        return OrderedDict([(
            'Log in to join the fun', ['No Completed Song Scores'])])
    elif (leaderboard_length == 0
            or leaderboard_length >= len(names_in_order)):
        # Return all players and songs if called with 'leaderboard_length'
        # of zero, if called with a 'leaderboard_length' higher than the
        # number of names return all
        return songs_scores_per_player_order
    else:
        # if the number of players is higher than the 'leaderboard_length'
        # return the amount requested
        sliced = islice(
            songs_scores_per_player_order.items(), leaderboard_length)
        sliced_o = OrderedDict(sliced)

        return sliced_o


def generate_logged_in_leaderboard(leaderboard_length):
    '''create a leaderboard of n length'''

    # select all player naames
    all_players = file_operations.read_from_file('data/players.txt')
    # create a list of player names ordered by total score desceding
    names_in_order = create_list_all_players_names_logged_in(all_players)
    # create a list of each players songs in the same order as 'names_in_order'
    songs_scores_per_player_order = create_song_list_each_name(names_in_order)

    if (len(names_in_order) == 0):
        # return placeholders if no players
        return OrderedDict([(
            'Log in to join the fun', ['No Completed Song Scores'])])
    elif (leaderboard_length == 0
            or leaderboard_length >= len(names_in_order)):
        # Return all players and songs if called with 'leaderboard_length'
        # of zero, if called with a 'leaderboard_length' higher than the
        # number of names return all
        return songs_scores_per_player_order
    else:
        # if the number of players is higher than the 'leaderboard_length'
        # return the amount requested
        sliced = islice(
            songs_scores_per_player_order.items(), leaderboard_length)
        sliced_o = OrderedDict(sliced)

        return sliced_o
