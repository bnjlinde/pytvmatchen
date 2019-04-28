#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import argparse
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description='Get Swedish broadcast schedule\
 for football from tvmatchen.nu')
parser.add_argument("--nofgames", help="Number of games to display", type=int)
parser.add_argument("--allsports", help="Display all sports instead of just football", action="store_true")
args = parser.parse_args()

if args.allsports:
    r = requests.get("https://www.tvmatchen.nu/")
else:
    r = requests.get("https://www.tvmatchen.nu/fotboll/")
r.encoding = 'UTF-8'
c = r.content
soup = BeautifulSoup(c, "html.parser", from_encoding="utf-8")

matches = []
all = soup.find_all('li', {'class': 'day'})

for item in all:
    date = item.span.text
    for match in item.find_all('li', {'class': 'match'}):
        details = {}
        details['date'] = date
        if match.time.get('class') == ['livescore']:
            details['time'] = match.select('.hidden-time')[0].text
        else:
            details['time'] = match.time.text
        teams = match.find_all("a")
        details['hometeam'] = teams[0].text.split(" – ")[0]
        details['awayteam'] = teams[0].text.split(" – ")[-1].split("LIVE ")[0]
        channels = []
        get_chan = match.find_all('a', {'class': 'channel'})
        for x in range(0, len(get_chan)):
            try:
                channels.append(get_chan[x]['title'])
            except:
                pass
        try:
            details['league'] = match.find('a', {'class': 'league'}).text
        except:
            details['league'] = ""

        details['channels'] = channels
        matches.append(details)


if args.nofgames:
    counter = 0
    while counter < int(args.nofgames):
        try:
            match = matches[counter]
            for key, value in match.items():
                print("{} - {}".format(key, value))
            print("\n")
            counter += 1
        except IndexError:
            break

else:
    for x in matches:
        for key, value in x.items():
            print("{} - {}".format(key, value))
        print("\n")
