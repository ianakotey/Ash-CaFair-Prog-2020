# Author: Ian Akotey, Stephen Owusu
# Version: 1.0.0
# Python Version: 3.8.0

# Solution to Task 2

from sys import argv, version_info
from IO import validateNumArgs, validateFilePath
from IO import parseVirusData, getUnknownCaseData, output_task2
from libProcessMyData import extractCases, findSublist

'''Requires Python 3.8+'''
assert version_info >= (3, 8, 0), 'Please use python 3.8+'

# development mode allows running without additional args
Mode = 'Production'


def main():

    if Mode != 'Development':

        validateNumArgs(argv, 3)
        files = list(map(validateFilePath, argv[1:]))
    else:
        files = ["../Test Data/covid_data.csv", "../Test Data/partial_time_series.csv"]


    covid = parseVirusData(filepath=files[0])
    unknownCaseData = getUnknownCaseData(filepath=files[1])


    """
    Filter the countries based on whether the unknown case data
    belongs to the country
    Return a dictionary with all countries that match
    """

    matchedCountries = dict(
        filter( lambda x: x[1] != -1,
                map( lambda geoId: (geoId, findSublist(
                                            main=covid[geoId]['cases']['NewConfCases'],
                                            sub=unknownCaseData)
                                            ),
                                    covid
                                    )
                                )
                            )

    if len(matchedCountries):
        # just in case there are more matches, just pick one
        datakey = list(matchedCountries.keys())[0]

        startIndex = matchedCountries[datakey] + len(unknownCaseData) - 1

        # virus data[key] --> country name
        data = (covid[datakey]['CountryExp'],
        # virus [datakey] --> cases -> dates --> start of matched timeseries
                covid[datakey]['cases']['DateRep'][startIndex])
        
    else:
        data = ('', '')

    output_task2(data=data, inputFile=files[1])


if __name__ == "__main__":
    main()