#!/usr/bin/env python3.7
"""Xiaomi MIUI Stable fastboot script for android one devices"""

import json
from bs4 import BeautifulSoup
from requests import get
from humanize import naturalsize


DATA = []


def get_fastboot(miui_id):
    """Scrape latest available fastboot ROM from MIUI downloads page"""
    url = 'http://en.miui.com/download-{}.html'.format(miui_id)
    response = get(url)
    page = BeautifulSoup(response.content, 'html.parser')
    links = page.findAll('a', {"class": "btn_5"})
    for i in links:
        log = []
        link = i['href']
        file_size = naturalsize(int(get(link, stream=True).headers['Content-Length']))
        file = link.split('/')[-1]
        region = file.split('_')[1][:2]
        names = page.findAll('span', {"class": "tab"})
        if file.count('_') == 7:
            name = [j.text for j in names if region == j.text.split(' ')[2].lower()[:2]]
            device = ''.join(name)
        else:
            device = page.find('span', {"class": "tab"}).text
        version = link.split('/')[3]
        android = link.split('_')[-2]
        codename = file.split('_')[0]
        info = {}
        info.update({"android": android})
        info.update({"codename": codename})
        info.update({"device": device})
        info.update({"download": link})
        info.update({"filename": file})
        info.update({"size": file_size})
        info.update({"md5": "null"})
        info.update({"version": version})
        DATA.append(info)
        log.append(info)
        with open('stable_fastboot/' + file.split('_images')[0] + '.json', 'w', newline='\n') as output:
            json.dump(log[0], output, indent=1)


def main():
    """loop through MIUI downloads and get the link"""
    ids = ['333', '353', '354', '365']
    for device_id in ids:
        get_fastboot(device_id)
    # write all json to one file
    # with open('ao.json', 'w', newline='\n') as ao:
    #     json.dump(DATA, ao, indent=1)


if __name__ == '__main__':
    main()
