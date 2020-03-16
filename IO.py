# Author: Ian Akotey, Stephen Owusu
# Version: 1.0.0
# Python Version: 3.8.0

# Functions not related to I/O stored here

from collections import defaultdict
from csv import DictReader
from itertools import islice
from os import getcwd, path
from sys import  platform
from datetime import datetime
from pathlib import Path

# format symbol not consistent across platforms
zT = '#' if platform == 'win32' else '-'


def validateNumArgs(args: list, numArgs: int) -> None:
    """Validate that the proper number of arguments required are provided.

    Raises TypeError otherwise.
    """

    if not len(args) == numArgs:
        raise TypeError(
            f"Program requires {numArgs} arguments:" f" Got {len(args)} instead"
        )


def validateFilePath(filepath: str, relative: bool=True) -> path:
    """Validate the presence of a filepath

    Returns either the relative or absolute file path relative to
    current folder.
    Raises FileNotFoundError if filepath is invalid
    """

    if path.isfile((tmp := path.join(getcwd(), filepath))):
        return filepath if relative else tmp
    else:
        raise FileNotFoundError(f"File '{filepath}' cannot be found")


def parsePopulationData(filepath: str) -> defaultdict:
    """Parse population data from file.
    
    Returns a dictionary, each key being the country code
    """

    tmp = defaultdict(lambda: dict(Country="", Country_Code="", Population=0, Year=0))

    with open(filepath, mode="r") as popusFile:
        pops = DictReader(popusFile)

        for item in pops:
            item['Population'], item['Year'] = (
                int(item['Population']), int(item['Year'])
            )
            tmp[item["Country_Code"]] = item

    return tmp



def parseVirusData(filepath: str) -> defaultdict:
    """Parse Coronavirus cases data from a given CSV file.
    
    Returns a dictionary, each key being the GeoId
    """

    tmp = defaultdict(lambda: dict(cases=dict(DateRep=[],NewConfCases=[],NewDeaths=[]), 
                                    totalCases=0, 
                                    totalDeaths=0,
                                    CountryExp=''
                                    )
    )

    with open(filepath, mode="r") as virusFile:
        virus = DictReader(
            virusFile,
            fieldnames=["DateRep", "CountryExp", "NewConfCases", "NewDeaths", "GeoId"],
        )

        for item in islice(virus, 1, None):
            item["DateRep"], item["NewConfCases"], item["NewDeaths"] = (
                datetime.strptime(item["DateRep"], "%m/%d/%y"),
                int(item["NewConfCases"]),
                int(item["NewDeaths"]),
            )

            key = tmp[item["GeoId"]]

            if not key['CountryExp']: key['CountryExp'] = item['CountryExp']
            key["totalCases"] += item["NewConfCases"]
            key["totalDeaths"] += item["NewDeaths"]

            key['cases']['DateRep'].append(item['DateRep'])
            key['cases']['NewConfCases'].append(item['NewConfCases'])
            key['cases']['NewDeaths'].append(item['NewDeaths'])

    return tmp



def getUnknownCaseData(filepath: str) -> list:
    """Returns a list of data from a single-columned file specified"""

    with open(filepath, mode="r") as x:
        # Remove the Byte order mark(ï»¿), if it exists
        return [eval(line.replace('ï»¿', '')) for line in x.readlines()]


def output_task1(data: str, inputFile: str) -> None:
    """Write solution for Task 1 into a file"""

    with open( f"task1_solution-{Path(inputFile).stem}.txt", mode='w' ) as file:
        file.write(data)



def output_task2(data: tuple, inputFile: str) -> None:
    """Write solution for Task 2 into a file"""

    with open( f"task2_solution-{Path(inputFile).stem}.txt", mode='w' ) as file:
        file.write(f'{data[0]}\n{data[1].strftime(f"%{zT}m/%{zT}d/%y")}')

