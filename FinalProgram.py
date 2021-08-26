import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, date
import csv

shapeY = 300000
shapeX = 505
websiteRankings = np.zeros(shape=(shapeY,shapeX), dtype=int)
websiteRankings[:] = 100000

websiteList = []
#testSite = np.array(['facebook', 'google', 'zoom'])
#date1 = [[2,1,2],[1,2,1],[3,3,4]]
siteCounter=0
dayCounter=0
ewmaCounter=0
index=0
ewmaArr = []
interestingWebsite = False
interestingWebsite2 = False
interestingWebsite3 = False

def numpy_ewma_vectorized_v2(data, window):

    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha
    n = data.shape[0]

    pows = alpha_rev**(np.arange(n+1))

    scale_arr = 1/pows[:-1]
    offset = data[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)

    mult = data*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out

def relevantPeaks(data):
    #Tuplar blir fel och maste lista ut hur man gor med flera peaks pa samma stalle
    intWebArr = []
    globalPeak = np.min(data[np.nonzero(data)])
    globalPeakIndex = np.argwhere(data == globalPeak)
    globalPeakIndex2 = globalPeakIndex.flatten().tolist()


    for peak in globalPeakIndex2:

        if peak >= 415:
            interestingWebsite = True
        else:
            interestingWebsite = False
        intWebArr.append(interestingWebsite)

    if any(pnt == True for pnt in intWebArr):
        interestingWebsite3 = True
    else:
        interestingWebsite3 = False

    return [interestingWebsite3,globalPeak,globalPeakIndex2]

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2018, 11, 1)              #Change the date
end_date = date(2020, 03, 25)

for single_date in daterange(start_date, end_date):


    daterange = single_date.strftime("%Y-%m-%d")
    #print(daterange)

    try:
        with open('umbrella100k-'+daterange+'.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter = ';')
            for website in plots:
                index = []
                if (siteCounter < shapeY) and ((website[1] in websiteList) == False):
                    #websiteRankings[siteCounter][0] = website[1]
                    websiteList.append(website[1])
                    websiteRankings[siteCounter,dayCounter] = website[0]
                    #websiteRankings[siteCounter] = website
                    siteCounter = siteCounter + 1

                elif (website[1] in websiteList) == True:
                    #websiteRankings = websiteRankings[np.where(websiteRankings == web)][dayCounter]
                    #index = np.where(np.any(website[1]==websiteRankings,axis=1))
                    index = websiteList.index(website[1])
                    websiteRankings[index,dayCounter] = website[0]

    #if (website in websiteRankings)== True:
        #for elements in date1:
            #for things in elements:
            dayCounter = dayCounter +1

    except IOError:
        print("File not accessible")
    print dayCounter

try:
    d = open('Umbrella-relevant.csv','wb')
    csv_writer_object = csv.writer(d,delimiter=";")

    for row in websiteRankings:
        ewmaArr = numpy_ewma_vectorized_v2(row,100)
        siteInformation = relevantPeaks(ewmaArr)
        if siteInformation[0] == True:
            csv_writer_object.writerow((websiteList[ewmaCounter], siteInformation[1],
            siteInformation[2]))
        ewmaCounter = ewmaCounter + 1

except IOError:
    print "Something went wrong"


print "Finished"
