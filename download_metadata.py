"""
Downloads metadata about Chicago Cubs opening day starters from
Basebase Reference.

Uses the CSV harvested by download_starters.py to do its thing.
"""
import csv
import time
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class Downloader(object):

    def __init__(self, data, delay=0.5):
        self.csv = list(csv.DictReader(data))
        headers = [
            'year', 'position', 'last_name', 'full_name', 'id', 'url',
            'birthplace_url', 'birthplace_name', 'birthplace_is_usa',
        ]
        outfile = csv.DictWriter(
            open("./starters-with-metadata.csv", "a"),
            headers
        )
        for row in self.csv[350:]:
            d = self.get(row)
            pprint(d)
            outfile.writerow(d)
            time.sleep(delay)

    def get(self, row):
        """
        Fetch the metadata for this player from our source.
        """
        req = requests.get(row['url'])
        data = req.text
        soup = BeautifulSoup(data)
        birth_a = [a for a in soup.find_all(id='necro-birth')[0].find_all("a")
            if a['href'].endswith('_born.shtml')][0]
        row.update({
            'birthplace_url': 'http://baseball-reference.com%s' % birth_a['href'],
            'birthplace_name': birth_a.contents[0].strip(),
            'birthplace_is_usa': len(birth_a.contents[0].strip()) == 2
        })
        return row


if __name__ == '__main__':
    dler = Downloader(open("./starters.csv", "rb"))
