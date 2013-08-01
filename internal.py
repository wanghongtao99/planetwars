"""Utility functions that are used for things besides game logic."""

import os.path
from collections import OrderedDict

import planetwars
from planetwars import Fleet, Planet

MAP_DIR = os.path.join(os.path.dirname(planetwars.__file__), "maps")

def load_map(map_file):
    planets = []
    fleets = []
    with open(map_file) as f:
        for line in f:
            line = line[:line.find("#")]
            tokens = line.split()
            if not tokens:
                continue
            elif tokens[0] == "P":
                x = float(tokens[1])
                y = float(tokens[2])
                owner = int(tokens[3])
                ships = int(tokens[4])
                growth = int(tokens[5])
                planets.append(Planet(len(planets), x, y, owner, ships, growth))
            elif tokens[0] == "F":
                owner = int(tokens[1])
                ships = int(tokens[2])
                source = int(tokens[3])
                destination = int(tokens[4])
                total_turns = int(tokens[5])
                remaining_turns = int(tokens[6])
                fleets.append(Fleet(owner, ships, source, destination,
                                    total_turns, remaining_turns))
    return planets, fleets

def all_maps():
    maps = OrderedDict()
    for dirpath, _, filenames in os.walk(MAP_DIR):
        for filename in filenames:
            map_path = os.path.join(dirpath, filename)
            map_name = os.path.splitext(map_path[len(MAP_DIR) + 1:])[0]
            maps[map_name] = load_map(map_path)
    return maps

roman_numerals = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V':5, 'I': 1}

def is_roman_numeral(s):
    for c in s:
        if c not in roman_numerals:
            return False
    return True

def roman_to_int(s):
    s = s.upper()
    if not is_roman_numeral(s):
        raise ValueError("Input is not a valid roman numeral: %s" % s)
    n = 0
    for i, c in enumerate(s):
        v = roman_numerals[c]
        if i < len(s) - 1 and roman_numerals[s[i + 1]] > v:
            n -= v
        else:
            n += v
    return n

def better_sort_key(s):
    tokens = s.split()
    new_tokens = []
    for token in tokens:
        try:
            new_tokens.append("%09d" % int(token))
        except ValueError:
            try:
                new_tokens.append("%09d" % roman_to_int(token))
            except ValueError:
                new_tokens.append(token)
    return " ".join(new_tokens)
