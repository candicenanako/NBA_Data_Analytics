import pandas as pd

# get columns of .csv file
def getColumns(input_file):
    with open(input_file, "r",encoding='utf-8') as dataFile:
        line = dataFile.readline()
        columns=line[:-1].split(',')
        return columns

# function that could print the count of unique values for each column
def printUniqueCount(dataFrame,columns):
    for item in columns:
        itemList = pd.unique(dataFrame[item])
        print("column \'"+ item +"\' unique values counts: ",len(itemList))

if __name__ == '__main__':
    files=['tweets_timelines.csv','tweets_keywords.csv']
    for file in files:
        # read csv file
        myData = pd.read_csv(file, sep=',', encoding='utf-8')
        print(myData)
        col=getColumns(file)[1:]
        print(col)
        printUniqueCount(myData,col)
        for c in col:
            valueCounts = myData[c].value_counts()
            empty= myData[myData[c] == None]
            # print(valueCounts)
            # print rate of None value
            print('for column '+ c +" :",len(empty) / len(myData))



