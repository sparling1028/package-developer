# This is a package managed, and written by the "package_developer" package.
# Code should not be changed manually, but only by the methods provided in the "package_developer" package.
# 
# "Package_developer" is copyrighted 2022 by Solomon Sparling under the GNU General Public License, Version 3.
# 
# I hope you get as much value out of this as possible.
# The world is full of opportunities; and the automation of data processes, I think, is the biggest one.


#  +-----------------------------------------------------------------------------------------------------------------+
#  |-----------------------------------------------------------------------------------------------------------------|
#  |-----------------------------------------------------------------------------------------------------------------|
#  |  888b     d888             888        888           8888888                                    888              |
#  |  8888b   d8888             888        888             888                                      888              |
#  |  88888b.d88888             888        888             888                                      888              |
#  |  888Y88888P888 .d88b.  .d88888888  888888 .d88b.      888  88888b.d88b. 88888b.  .d88b. 888d888888888.d8888b    |
#  |  888 Y888P 888d88""88bd88" 888888  888888d8P  Y8b     888  888 "888 "88b888 "88bd88""88b888P"  888   88K        |
#  |  888  Y8P  888888  888888  888888  88888888888888     888  888  888  888888  888888  888888    888   "Y8888b.   |
#  |  888   "   888Y88..88PY88b 888Y88b 888888Y8b.         888  888  888  888888 d88PY88..88P888    Y88b.      X88   |
#  |  888       888 "Y88P"  "Y88888 "Y88888888 "Y8888    8888888888  888  88888888P"  "Y88P" 888     "Y888 88888P'   |
#  |                                                                         888                                     |
#  |                                                                         888                                     |
#  |                                                                         888                                     |
#  |-----------------------------------------------------------------------------------------------------------------|
#  |-----------------------------------------------------------------------------------------------------------------|
#  +-----------------------------------------------------------------------------------------------------------------+

import time
import os
import extcolors

import numpy as np

from selenium.webdriver.chrome.options import Options as chrome_options
from selenium import webdriver


#  +--------------------------------------------------------------------------------------------------------------------------------+
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  |  888b     d888             888        888                  d8888888   888          d8b888             888                      |
#  |  8888b   d8888             888        888                 d88888888   888          Y8P888             888                      |
#  |  88888b.d88888             888        888                d88P888888   888             888             888                      |
#  |  888Y88888P888 .d88b.  .d88888888  888888 .d88b.        d88P 888888888888888888d88888888888b. 888  888888888 .d88b. .d8888b    |
#  |  888 Y888P 888d88""88bd88" 888888  888888d8P  Y8b      d88P  888888   888   888P"  888888 "88b888  888888   d8P  Y8b88K        |
#  |  888  Y8P  888888  888888  888888  88888888888888     d88P   888888   888   888    888888  888888  888888   88888888"Y8888b.   |
#  |  888   "   888Y88..88PY88b 888Y88b 888888Y8b.        d8888888888Y88b. Y88b. 888    888888 d88PY88b 888Y88b. Y8b.         X88   |
#  |  888       888 "Y88P"  "Y88888 "Y88888888 "Y8888    d88P     888 "Y888 "Y888888    88888888P"  "Y88888 "Y888 "Y8888  88888P'   |
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  +--------------------------------------------------------------------------------------------------------------------------------+

end_format = '[0m'

bold = '[1m'

underline = '[4m'

#  +------------------------------------------------------------------------------------------------------------------------+
#  |------------------------------------------------------------------------------------------------------------------------|
#  |------------------------------------------------------------------------------------------------------------------------|
#  |  888b     d888             888        888           8888888888                     888   d8b                           |
#  |  8888b   d8888             888        888           888                            888   Y8P                           |
#  |  88888b.d88888             888        888           888                            888                                 |
#  |  888Y88888P888 .d88b.  .d88888888  888888 .d88b.    8888888888  88888888b.  .d8888b888888888 .d88b. 88888b. .d8888b    |
#  |  888 Y888P 888d88""88bd88" 888888  888888d8P  Y8b   888    888  888888 "88bd88P"   888   888d88""88b888 "88b88K        |
#  |  888  Y8P  888888  888888  888888  88888888888888   888    888  888888  888888     888   888888  888888  888"Y8888b.   |
#  |  888   "   888Y88..88PY88b 888Y88b 888888Y8b.       888    Y88b 888888  888Y88b.   Y88b. 888Y88..88P888  888     X88   |
#  |  888       888 "Y88P"  "Y88888 "Y88888888 "Y8888    888     "Y88888888  888 "Y8888P "Y888888 "Y88P" 888  888 88888P'   |
#  |------------------------------------------------------------------------------------------------------------------------|
#  |------------------------------------------------------------------------------------------------------------------------|
#  +------------------------------------------------------------------------------------------------------------------------+

def extract_colors(filename, n=5, tolerance=30, max_brightness = 100):
    # we want to end up with n colors, but certain shades of gray will be removed
    # therefore we will need to try a few different limits before we end up with n colors
    limit = n
    colors = []
    while len(colors) < n:
        print(f"{len(colors) = }")
        colors = extcolors.extract_from_path(filename, limit=limit)
        if limit < 2 * n:
            colors = [tup for tup, count in colors[0] if (len(set(tup)) == 3) & (min(tup) < max_brightness)]
        elif limit < 4 * n:
            colors = [tup for tup, count in colors[0] if (len(set(tup)) == 3) & (min(tup) < max_brightness)]
            tolerance = .85 * tolerance
            max_brightness = 1.2 * max_brightness
        else:
            assert False, f"could not find {n} colors"
            
        limit += 1
    print(f"found {len(colors)} colors")
    return [f"\033[38;2;{r};{g};{b}m" for r, g, b in colors]



#  +-----------------------------------------------------------------------------------------------------------+
#  |-----------------------------------------------------------------------------------------------------------|
#  |-----------------------------------------------------------------------------------------------------------|
#  |                          888                            .d888                                    888      |
#  |                          888                           d88P"                                     888      |
#  |                          888                           888                                       888      |
#  |   .d8888b888  888.d8888b 888888 .d88b. 88888b.d88b.    888888 .d88b. 888d88888888b.d88b.  8888b. 888888   |
#  |  d88P"   888  88888K     888   d88""88b888 "888 "88b   888   d88""88b888P"  888 "888 "88b    "88b888      |
#  |  888     888  888"Y8888b.888   888  888888  888  888   888   888  888888    888  888  888.d888888888      |
#  |  Y88b.   Y88b 888     X88Y88b. Y88..88P888  888  888   888   Y88..88P888    888  888  888888  888Y88b.    |
#  |   "Y8888P "Y88888 88888P' "Y888 "Y88P" 888  888  888   888    "Y88P" 888    888  888  888"Y888888 "Y888   |
#  |-----------------------------------------------------------------------------------------------------------|
#  |-----------------------------------------------------------------------------------------------------------|
#  +-----------------------------------------------------------------------------------------------------------+

class custom_format:


    def __init__(self, search_or_site, n=5, tolerance=30, max_brightness=100, ):
        """
    Scrapes the most fequent colors of of a website, and constructs custom print functions based on those colors.
    If search or site looks like a website ([https://]words.words.words) it will search that landing page.
    If it is a search page it will scrape from the first non-add return from google.
        """
        self.screenshot_homepage(search_or_site)
        self.colors = extract_colors(self.image_file, n=n, tolerance=tolerance, max_brightness=max_brightness)
        self.delete_image_file()




    def __str__(self):
        if self.__bold__:
            _bold = bold
        else:
            _bold = ''
        #---------------
        if self.__underline__:
            _underline = underline
        else:
            _underline = ''
        #---------------
        if self.__color__ == False:
            _color = ''
        else:
            _color = self.colors[self.__color__-1]
        return _bold + _underline + _color + self.__text__ + end_format




    def __repr__(self):
        return str(self)




    def print_colors(self, text=None):
        if (text == None) & hasattr(self, '__text__'):
            text = self.__text__
        elif text == None:
            text = 'Hello'
        for color in self.colors:
            print(color + text + end_format)
        return self




    def reset_palette(self, search_or_site, n=5, tolerance=30, max_brightness=100, ):
        """
    Scrapes the most fequent colors of of a website, and constructs custom print functions based on those colors.
    If search or site looks like a website ([https://]words.words.words) it will search that landing page.
    If it is a search page it will scrape from the first non-add return from google.
        """
        self.screenshot_homepage(search_or_site)
        self.colors = extract_colors(self.image_file, n=n, tolerance=tolerance, max_brightness=max_brightness)
        self.delete_image_file()
        return self




    def return_nan(self):
        return np.nan




    def text(self, text, bold=False, underline=False, color=0):
        self.__text__ = text
        self.__bold__ = bold
        self.__underline__ = underline
        self.__color__ = color
        return self





#  +-----------------------------------------------+
#  |   _                           _               |
#  |  | |                         (_)              |
#  |  | |__  _ __ _____      _____ _ _ __   __ _   |
#  |  | '_ \| '__/ _ \ \ /\ / / __| | '_ \ / _` |  |
#  |  | |_) | | | (_) \ V  V /\__ \ | | | | (_| |  |
#  |  |_.__/|_|  \___/ \_/\_/ |___/_|_| |_|\__, |  |
#  |                                        __/ |  |
#  |                                       |___/   |
#  +-----------------------------------------------+
#  method group: browsing

    def delete_image_file(self):
        os.remove(self.image_file)
        return self




    def screenshot_homepage(self, website):
        options = chrome_options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        if '.' not in website:
            domains = ['com', 'org', 'gov', 'net', 'co', 'io']
            for domain in domains:
                try:
                    site_name = f"https://www.{website}.{domain}"
                    driver.get(site_name)
                    print(f'found site {site_name}')
                    break
                except:
                    pass
                assert False, "couldn't find website, please input url directly"
        else:
            driver.get(website)
        # wait a few seconds
        time.sleep(5)
        # save screenshot of landing page
        self.image_file = 'some-ridiculous-name-that-wont-clash-with-anything-else-asdkgjbenasdkgfhjasdf.png'
        driver.get_screenshot_as_file(self.image_file)
        print('screenshot saved')
        return self





#  +---------------------------------------------------------+
#  |    __                           _   _   _               |
#  |   / _|                         | | | | (_)              |
#  |  | |_ ___  _ __ _ __ ___   __ _| |_| |_ _ _ __   __ _   |
#  |  |  _/ _ \| '__| '_ ` _ \ / _` | __| __| | '_ \ / _` |  |
#  |  | || (_) | |  | | | | | | (_| | |_| |_| | | | | (_| |  |
#  |  |_| \___/|_|  |_| |_| |_|\__,_|\__|\__|_|_| |_|\__, |  |
#  |                                                  __/ |  |
#  |                                                 |___/   |
#  +---------------------------------------------------------+
#  method group: formatting

    def color(self, n=1):
        if n in {None, 0, False}:
            self.__color__ = False
        else:
            self.__color__ = n
        return self




    def bold(self, bold=True):
        self.__bold__ = bold
        return self




    def title(self, n=1):
        # if not already surrounded by underscores
        if self.__text__[:2] + self.__text__[-2:] != '____':
            self.__text__ = f"__{self.__text__}__"
        return self.bold().underline().color(n)




    def underline(self, underline=True):
        self.__underline__ = underline
        return self





