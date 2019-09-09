#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup


class MatchList():
    def __init__(self):
        self.matches = []

    def get_matches(self, *, allsports: bool=True):
        if allsports:
            self.r = requests.get("https://www.tvmatchen.nu/")
        else:
            self.r = requests.get("https://www.tvmatchen.nu/fotboll")

        self.r.encoding = 'UTF-8'
        self.c = self.r.content
        self.soup = BeautifulSoup(self.c, 'html.parser', from_encoding='utf-8')
        self.all = self.soup.find_all('li', {'class': 'day'})

        for item in self.all:
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
                details['league'] = self.match.find('a', {'class': 'league'}).text
            except:
                details['league'] = ""

            details['channels'] = channels
            self.matches.append(details)
        return self.matches

    def pretty_print(self, nofgames: int=20):
        if len(self.matches) == 0:
            self.get_matches()
        stringofgames = ""
        counter = 0
        while counter < nofgames:
            try:
                match = self.matches[counter]
                for key, value in match.items():
                    stringofgames += "{} - {}\n".format(key, value)
                stringofgames += "\n"
                counter += 1
            except IndexError:
                break
        return stringofgames


if __name__ == '__main__':
    m = MatchList()
    print(m.pretty_print(nofgames=10))
    print("-----------------\nEnd of list")
