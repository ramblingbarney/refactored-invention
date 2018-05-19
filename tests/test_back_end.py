import unittest
import music
from random import randint, random
import json

class TestMusic(unittest.TestCase):

    '''
    Our test suite for Guess the next line
    '''
    def test_video_lyric_json_steam(self):

        # List of videos which lyrics are provided by MusixMatch
        pre_canned_videoId = ['YQHsXMglC9A','0-EF60neguk','MN3x-kAbgFU','YR5ApYxkU-U','n4RjJKxsamQ','raNGeq3_DtM','TvnYmWpD_T8','x5GuBa4Bbnw','4YR_Mft7yIM','JJAXwAaA2w','u1xrNaTO1bI','jhdFe3evXpk','YQHsXMglC9A']

        # generage a random number to select a video from the precanned list of known MusixMatch provided lyrics
        randomNumber = randint(0,len(pre_canned_videoId)- 1)

        def is_json(myjson):
            try:
                json_object = json.loads(myjson)
            except Exception as err:
                return False
            return True

        '''
        Test to see if we can generate a valid json lyric stream
        '''

        # get unprocessed lyrics stream
        rawlyric = music.fetch_srt('xxx',pre_canned_videoId[randomNumber])

        # process lyric stream and format to json
        lyric = music.convert_srt(rawlyric)

        self.assertEqual(is_json(lyric),True)

    def test_video_lyric_json_lyrics(self):

        # List of videos which lyrics are provided by MusixMatch
        pre_canned_videoId = ['YQHsXMglC9A','0-EF60neguk','MN3x-kAbgFU','YR5ApYxkU-U','n4RjJKxsamQ','raNGeq3_DtM','TvnYmWpD_T8','x5GuBa4Bbnw','4YR_Mft7yIM','JJAXwAaA2w','u1xrNaTO1bI','jhdFe3evXpk','YQHsXMglC9A']

        # generage a random number to select a video from the precanned list of known MusixMatch provided lyrics
        randomNumber = randint(0,len(pre_canned_videoId)- 1)

        start_times = []

        end_times = []

        '''
        Test to see if we the generated lyric streams start and next end timestamp match
        '''

        # get unprocessed lyrics stream
        rawlyric = music.fetch_srt('xxx',pre_canned_videoId[randomNumber])

        # process lyric stream and format to json
        lyric = json.loads(music.convert_srt(rawlyric))

        keys_list = []
        startTimes = []
        endTimes = []

        for i in lyric[0]:
            keys_list.append(i)

        def is_full_time_sequence():
            for i in keys_list:

                startTimes.append(lyric[0][i]['timeStart'])
                endTimes.append(lyric[0][i]['timeEnd'])
            del startTimes[0]
            del endTimes[-1]

            return set(startTimes) == set(endTimes)

        self.assertEqual(is_full_time_sequence(),True)

    def test_video_lyrics_contain_strings(self):

        # List of videos which lyrics are provided by MusixMatch
        pre_canned_videoId = ['YQHsXMglC9A','0-EF60neguk','MN3x-kAbgFU','YR5ApYxkU-U','n4RjJKxsamQ','raNGeq3_DtM','TvnYmWpD_T8','x5GuBa4Bbnw','4YR_Mft7yIM','JJAXwAaA2w','u1xrNaTO1bI','jhdFe3evXpk','YQHsXMglC9A']

        # generage a random number to select a video from the precanned list of known MusixMatch provided lyrics
        randomNumber = randint(0,len(pre_canned_videoId)- 1)

        '''
        Test to see if we the generated lyric streams contain song lyrics
        '''

        # get unprocessed lyrics stream
        rawlyric = music.fetch_srt('xxx',pre_canned_videoId[randomNumber])

        # process lyric stream and format to json
        lyric = json.loads(music.convert_srt(rawlyric))

        def is_lyric_sequence():
            for i in lyric[1]:
                
                if ( len(i['lyric']) >= 2 & isinstance(i['lyric'], str) ):
                    True
                else:
                    return False
            return True

        self.assertEqual(is_lyric_sequence(),True)
