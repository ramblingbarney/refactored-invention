import file_operations
from collections import OrderedDict
from operator import itemgetter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def levestein_score(to_be_scored_string, answer):
    return fuzz.ratio(to_be_scored_string, answer)


def generate_leaderboard(leaderboard_length):

    class_list = ['bg-primary','bg-warning','bg-success','bg-danger']

    all_players = file_operations.read_from_file('data/players.txt')

    names_dict = {}

    names = []

    result = []

    # check for empty players file and return placeholder values for template display without further processing
    if ( len(list(all_players.values()) ) == 0):

        names = ["Log in to join the fun"]
        result = ["<li>No Completed Song Scores</li>"]

        return [names,class_list,result]

    # create a list of all players names

    for name in list(all_players.values()):

        name_array = name.split(",")

        names_dict[name_array[0]] = int(name_array[1])

        names = list(OrderedDict(sorted(names_dict.items(), key = itemgetter(1), reverse = True)).keys())

    for name in names:
        # select all songs by person, if no songs 'None' is returned
        raw_result = file_operations.search_from_file('data/song_scores.txt', name,1) # 0 returns the first result, 1 returns all results

        if ( raw_result is not None ):
            string = ""
            for key, value in raw_result.items():
                string += "<li>{0} - {1}</li>".format(value.split(",")[1],value.split(",")[2])
            result.append(string)
        else:
            result.append('<li>No Completed Song Scores</li>')

    # create list of classes which is longer than the names, extra is ignored in the template
    classes = class_list * (len(names))

    # if called with the same number of names in the song score file return all available names
    if ( leaderboard_length >= len(names) ):
        return [names,classes,result]
    elif ( leaderboard_length == 0 ):
        return [names,classes,result]
    else:
    # if called with less than the number of names in the song score file return then number requested
        return [names[:leaderboard_length],classes[:leaderboard_length],result[:leaderboard_length]]
