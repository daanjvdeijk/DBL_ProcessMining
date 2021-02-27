import statistics
from statistics import mode

class SimplePredict:
    def makeList(self):
        global list
        list = [1,2,6,6]

    def nexteventchance(self):
        modeNumber = mode(list)
        percentageOccurring = list.count(modeNumber)/len(list) * 100

        return percentageOccurring


object = SimplePredict()
temp = object.makeList()
print("The chance of a " + str(mode(list)) + " to occur is: " + str(object.nexteventchance()) + "%")
