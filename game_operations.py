import file_operations
from collections import OrderedDict
from operator import itemgetter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# this is a python implenentation of the published theory
# https://en.wikipedia.org/wiki/Levenshtein_distance
# I have used a library provided by SeatGeek
 #https://github.com/seatgeek/fuzzywuzzy
'''levenshtein string comparison'''

levenshtein_score = lambda to_be_scored_string, answer: fuzz.ratio(
    to_be_scored_string, answer)

# def levenshtein_score(to_be_scored_string, answer):
#
#     song_score = fuzz.ratio(to_be_scored_string, answer)
#
#     return song_score

def create_list_all_players_names(all_game_players):

    '''create a list of all players names'''

    names_dict = {}

    for name in list(all_game_players.values()):

        name_array = name.split(",")

        # add to a dictionary by player name as key and score as value
        names_dict[name_array[0]] = int(name_array[1])

    # sort names dictionary by value
    sorted_names_dict = sorted(names_dict.items(),
        key = itemgetter(1), reverse = True)

    ordered_player_names = list(OrderedDict(sorted_names_dict).keys())

    return ordered_player_names

def create_song_list_each_name(names):

    '''create a list of songs and scores per name'''

    name_songs_with_scores = []

    for name in names:
        # select all songs by person, if no songs 'None' is returned
        # 'first' returns the first result, 'all' returns all results
        raw_result = file_operations.search_from_file(
        'data/song_scores.txt', name,'all')

        if ( raw_result is not None ):

            for key, value in raw_result.items():

                name_songs_with_scores.append(
                    "{0} - {1}".format(value.split(",")[1],value.split(",")[2]))

        else:

            name_songs_with_scores.append('No Completed Song Scores')

    return name_songs_with_scores

def generate_leaderboard(leaderboard_length):

    '''create a leaderboard of n length'''

    all_players = file_operations.read_from_file('data/players.txt')

    # check for empty players file and return placeholder values for template
    # display without further processing
    if ( leaderboard_length == 0 ):

        return [['Log in to join the fun'],['No Completed Song Scores']]

    elif ( len(list(all_players.values()) ) == 0 ):

        return [['Log in to join the fun'],['No Completed Song Scores']]

    names_in_order = create_list_all_players_names(all_players)

    songs_scores_per_player_order = create_song_list_each_name(names_in_order)

    # if called with the same number of names in the song score file return all available names
    if ( leaderboard_length >= len(names_in_order) ):
        return [names_in_order,songs_scores_per_player_order]
    else:
    # if called with less than the number of names in the song score file return then number requested
        return [names_in_order[:leaderboard_length],songs_scores_per_player_order[:leaderboard_length]]
