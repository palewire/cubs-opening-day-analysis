"""
Downloads the complete list of Chicago Cubs opening day starters from
Basebase Reference in CSV format

Source: http://www.baseball-reference.com/teams/CHC/opening.shtml
"""
import csv
import requests
from bs4 import BeautifulSoup


class Downloader(object):

    def _scrape_player_cell(self, td):
        """
        Accepts a <td> tag from the Baseball Reference source table that
        contains data about a player and extracts out the bits we want.

        Returns a dictionary.
        """
        return {
            'id': td.a['data-entry-id'].strip(),
            'url': 'http://baseball-reference.com%s' % td.a['href'],
            'full_name': td.a['title'],
            'last_name': td.a.contents[0]
        }

    def get(self):
        """
        Scrapes the data from our source. Returns a list of dictionaries.
        """
        outfile = csv.DictWriter(
            open("./starters.csv", "wb"),
            ['year', 'position', 'last_name', 'full_name', 'id', 'url']
        )
        url = 'http://www.baseball-reference.com/teams/CHC/opening.shtml'
        req = requests.get(url)
        data = req.text
        soup = BeautifulSoup(data)
        tbody = soup.find_all("tbody")[0]
        position_order = [
            'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P'
        ]
        for tr in tbody.find_all("tr"):
            cells = tr.find_all("td")
            year = int(cells[0].a['name'])
            for i, position in enumerate(position_order):
                data = self._scrape_player_cell(cells[i+1])
                data.update({
                    'year': year,
                    'position': position,
                })
                outfile.writerow(data)

if __name__ == "__main__":
    dler = Downloader()
    dler.get()
