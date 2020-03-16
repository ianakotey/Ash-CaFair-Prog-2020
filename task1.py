# Author: Ian Akotey, Stephen Owusu
# Version: 1.0.0
# Python Version: 3.8.0

from functools import reduce
from sys import argv, version_info
from IO import zT, validateNumArgs, validateFilePath
from IO import  parseVirusData, parsePopulationData, output_task1
from libProcessMyData import getLatestCases, lineOfBestFit, extractCases
import operator
from json import loads
from collections import defaultdict



'''Requires Python 3.8+'''
assert version_info >= (3,8,0), 'Please use python 3.8+'

Mode = 'Development'

def main():


    if Mode != 'Development':

        validateNumArgs(argv, 3)

        files = list(map(validateFilePath, argv[1:]))
    else:
        files = ["../Test Data/covid_data.csv", "../Test Data/population_data.csv"]




    covid = parseVirusData(filepath=files[0])
    countryInfo = parsePopulationData(filepath=files[1])


    # load geoId -> Country Code mapping
    with open('mapping.json') as jsonData:

        mapping = loads(jsonData.read())

        mapping = defaultdict(str, mapping)
        mapping['EL'] = 'GRC' # patch missing link to Greece


    # sort by number of new infection
    countriesSortedByInfection = sorted(covid,
                                        key=lambda geoId: covid[geoId]['totalCases'],
                                        reverse=True
    )

    # sort by infection rate (totalCases/Population)
    countriesSortedbyInfectionRate = sorted(covid,
        key=lambda geoId: covid[geoId]['totalCases'] \
                          /tmp
                        if (tmp := countryInfo[mapping[geoId]]['Population']) != 0
                        # if population does not exist, return 0
                        else 0,
        reverse=True
    )

    # sort by Death rate (totalDeath/totalCases)
    countriesSortedbyDeathRate = sorted(covid,
                                    key=lambda geoId: covid[geoId]['totalDeaths'] \
                                                      /covid[geoId]['totalCases'],
                                    reverse=True
    )

    # solsdcd - Slope of last seven days case data for every country
    # needed for trend analysis
    solsdcd = dict( map(
                        lambda geoId:
                                    (geoId,
                                     lineOfBestFit(
                                                dataX=range(8, 1, -1),
                                                dataY=covid[geoId]['cases']['NewConfCases'][:7]
                                                   )
                                    ),
                         covid
                        )
    )


    countriesWithIncrease = sorted(
        [key for key in solsdcd if solsdcd[key] > 0],
        key=lambda key: solsdcd[key],
        reverse=True
    )

    countriesWithDecrease = sorted(
        [key for key in solsdcd if solsdcd[key] < 0],
        key=lambda key: solsdcd[key],
    )

    # cdwiomamv - country data with index of max and max value
    # useful in early peak calculations

    # cdwiomamv = {'geoId': (index of peak, peak value)}

    cdwiomamv = dict(map(lambda geoId:
                                (geoId,
                                 max(
                                     list(enumerate(covid[geoId]['cases']['NewConfCases']))[::-1],
                                     key=lambda item: item[1]
                                     )
                                 ),
                         countriesWithDecrease
                        )
    )


    # get the country code of the country that peaked first
    # by finding the country with the lowest peak date
    firstPeakCountryCode = min(cdwiomamv,
                    # covid[geoId] -> cases -> dates -> dates[index of peak date]
                                key = lambda geoId: covid[geoId]['cases'] \
                                                         ['DateRep'][cdwiomamv[geoId][0]]
    )


    # Solutions follow, using data above


    # covid[highest infected] --> cases --> first case --> (country, totalCases)
    part1 = (covid[countriesSortedByInfection[0]]['CountryExp'],
             covid[countriesSortedByInfection[0]]['totalCases'])


    # covid[highest infected] --> cases --> second case --> (country, totalCases)
    part2 = (covid[countriesSortedByInfection[1]]['CountryExp'],
             covid[countriesSortedByInfection[1]]['totalCases'])


    mostInfectedCountryKey = countriesSortedbyInfectionRate[0]
    mostInfectedCountry = covid[mostInfectedCountryKey]

    part3 = (mostInfectedCountry['CountryExp'],

             mostInfectedCountry['totalCases'] \
             / countryInfo[mapping[mostInfectedCountryKey]]['Population'])


    # sum(all totalDeaths)/sum(all totalCases)
    part4 = reduce(operator.add, map(lambda geoId: covid[geoId]['totalDeaths'], covid)) \
            /reduce(operator.add, map(lambda geoId: covid[geoId]['totalCases'], covid))



    highestDeathRateCountryKey = countriesSortedbyDeathRate[0]
    highestDeathRateCountry = covid[highestDeathRateCountryKey]

    part5 = (highestDeathRateCountry['CountryExp'],

            highestDeathRateCountry['totalDeaths'] \
            /highestDeathRateCountry['totalCases'])



    part6 = tuple(map(lambda country: covid[country]['CountryExp'],
                      countriesWithIncrease
                      )
    )




    # It's sorted, just pick the first one
    part7 = part6[0]



    part8 = tuple(map(lambda country: covid[country]['CountryExp'],
                    countriesWithDecrease)
                 )



    # It's sorted, just pick the first one
    part9 = part8[0]


    # covid[firstPeak...] -> case -> earliest peaking case
    # fPCC -> first PeakCountry Code]
    fPCC = cdwiomamv[firstPeakCountryCode][0]

    part10 = (covid[firstPeakCountryCode]['CountryExp'],
              covid[firstPeakCountryCode]['cases']['DateRep'][fPCC])


    solution = f"(a) {part1[0]},{part1[1]}\n" \
               f"(b) {part2[0]},{part2[1]}\n" \
               f"(c) {part3[0]},{part3[1]}\n" \
               f"(d) {part4}\n" \
               f"(e) {part5[0]},{part5[1]}\n" \
               f"(f) {','.join(part6)}\n" \
               f"(g) {part7}\n" \
               f"(h) {','.join(part8)}\n" \
               f"(i) {part9}\n" \
               f"(j) {part10[0]},{part10[1].strftime(f'%{zT}m/%{zT}d/%y')}"

    output_task1(data=solution, inputFile=files[0])



if __name__ == "__main__":
    main()
    from timeit import repeat
    print( repeat('main()', repeat=3, number=10) )
