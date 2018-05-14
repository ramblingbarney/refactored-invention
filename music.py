from html.parser import HTMLParser
import json
import requests
import time
import datetime
import re



def fetch_srt(song_name,video_id):

    video_id = video_id

    #preparing the first parameter
    res = 'A'.join(str(ord(c)+13) for c in video_id)

    # Fake a request to get a cookie

    session = requests.Session()
    session.get('https://extension.musixmatch.com')

    #HTTP request with http header values

    url = "https://extension.musixmatch.com/?res="+res+"&hl=en-US&v="+video_id+"&type=track&lang=en&name&kind&fmt=1"

    headers = {
        "Origin": "https://www.youtube.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "X-YouTube-Page-Label": "youtube.ytfe.desktop_20180222_0_RC3",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",
        "X-YouTube-Variants-Checksum": "ada5c2c76a207cc7ea9fd948091f2776",
        "Accept": "*/*",
        "X-YouTube-Page-CL": "186658434",
        "Referer": "https://www.youtube.com/",
        "X-YouTube-Client-Name": "1",
        "X-YouTube-Client-Version": "2.20180222",
        "Connection": "keep-alive",
    }

    response = session.get(url, headers=headers)

    return response.text

def convert_srt(raw_text):

    TIME_FORMAT2 = "%H:%M:%S,%f"
    formattedTime0 = time.mktime(time.strptime("00:00:00,000", TIME_FORMAT2))

    h = HTMLParser()
    cnt=0
    flag=0
    s = raw_text.split("text")
    str_name = "k.srt"

    times = {}
    values_list_lyric = []
    for i in s:
        if cnt%2==1:
			#print (i)
            flag  = flag+1
            # srt_string = srt_string+str(flag)+"\n"
            s2 = i.split('"')
            c = h.unescape(s2[4])
            c2 = re.sub(r'&apos;',"&#39;", c[1:len(c)-2], re.IGNORECASE) # amended original code to replace &apos; with &#39; as the former is not included on the list of HTML entities
            end = float(s2[1])+float(s2[3])
            if "." in s2[1]:
                x1 = s2[1].split(".")
                ms1 = x1[1]
                while len(ms1)<3:
                    ms1+="0"
                x = float(x1[0])
            else :
                ms1="000"
                x = float(s2[1])
            if "." in s2[3]:
                y1 = s2[3].split(".")
                ms2 = y1[1]
                while len(ms2)<3:
                    ms2+="0"
                y = float(x1[0])
            else:
                ms2="000"
                y = float(s2[1])

            end1= str(end)
            if "." in end1:
                x3 = end1.split(".")
                ms3 = x3[1]
                x4  = float(x3[0])
            else:
                ms3="000"
                x4 = float(end1)
            m, s = divmod(x, 60)
            h1, m = divmod(m, 60)

			# convert end time in ms,s,m,h format
            m2,s2 = divmod(x4,60)
            h2,m2 =divmod(m2,60)

            t1 = "%02d:%02d:%02d,%.3s" % (h1, m, s,ms1)
            t2 = "%02d:%02d:%02d,%.3s" % (h2,m2,s2,ms3)
            formattedTime1 = time.mktime(time.strptime(t1, TIME_FORMAT2))
            formattedTime2 = time.mktime(time.strptime(t2, TIME_FORMAT2))

            tDelta2 = formattedTime2 -  formattedTime1
            tDelta1 = formattedTime1 - formattedTime0

            times[cnt]= {"timeStart": int(tDelta1)*1000, "timeEnd":int(tDelta1 + tDelta2)*1000}
            values_list_lyric.append({"_id": str(cnt), "lyric": c2 })
        cnt = cnt+1


    return json.dumps([times,values_list_lyric])

# x = fetch_srt("Christy Moore - Weekend in Amsterdam","YQHsXMglC9A")
# print(convert_srt(x))
