# Author: Ian Akotey, Stephen Owusu
# Version: 1.0.0
# Python Version: 3.8.0
# Named after the linux library libEatMyData
# Additional functions not related to I/O stored here

from itertools import zip_longest
from sys import maxsize
from statistics import mean


def groupItems(data, n):
    return zip_longest(*([iter(data)] * n), fillvalue=maxsize)


def increasingTrend(data: list) -> bool:
    '''
    Returns True if d[0]<d[1]<d[2]<...d[last]
    for input iterable d
    '''
    for i in range(1, len(data)):
        if data[i] < data[i - 1]:
            return False
    return True


def decreasingTrend(data: list) -> bool:
    '''
    Returns True if d[0]>d[1]>d[2]>...d[last]
    for input iterable d
    '''
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            return False
    return True


def lineOfBestFit(dataX, dataY, gradientOnly: bool = True):
    """Return line of best fit to data points provided
    Returns gradient only by default"""

    if not dataX: raise ValueError('Empty list provided')
    dataY = dataY + [0]*(len(dataX)-len(dataY))
    if len(dataX) == 1: return dataY[0]

    mx, my = mean(dataX), mean(dataY)
    mxx = mean(map(lambda x: x**2, dataX))
    mxy = mean(map(lambda x: x[0] * x[1], zip(dataX, dataY)))

    try:

        m = (mx*my - mxy) \
            /(mx*mx - mxx)
    except ZeroDivisionError:
        m = maxsize
    return m if gradientOnly else (m, my - m*mx)


def getLatestCases(virusData: dict, geoId: str, n: int = 1, latestFirst: bool = True) -> list:
    """Return latest n cases for a given geoId"""
    answer =  list(
        map(lambda case: case['NewConfCases'], virusData[geoId]['cases'][:n])
    )


    return answer[::(1 if latestFirst else -1)]




def extractCases(virusData: dict, geoId: str) -> list:
    return list(
        map( lambda case: case['NewConfCases'], virusData[geoId]['cases'] )
    )


def listEqual(list1: list, list2: list) -> bool:
    '''Checks whether two lists are equal'''
    return len(list1) == len(list2) and \
           all( map( lambda item:item[0]==item[1], zip(list1, list2) ) )


def findSublist(main: list, sub: list) -> int:
    '''Searches for a sublist in a given list
        Returns start index of sublist or -1 if not found'''
    for _ in range(len(main) - (tmp := len(sub)) + 1):
        if listEqual(main[_:_+tmp], sub):
            return _
    else:
        return -1



