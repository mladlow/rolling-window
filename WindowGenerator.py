#!/usr/bin/python

# Averages: use linked list, track the sum, most sane LL implementations track the size of your LL for you. When you put a new value into your LL, pop a value off the front, and adjust your sum accordingly. This is O(n).

# Maximums: to get something that works, the method I'm using iterates over the list, adding to a linked list and storing the maximum. If you remove the maximum, this will find a new maximum in the list. Because our windows sizes are so small, this is still O(n) - with large window sizes you'd want to do something smarter.

from collections import deque

# The SmartDeque tracks the size of the deque (I wasn't sure about the maxlen
# behavior - would the append function return what was popped when maxlen was 
# exceeded), the sum of the deque, and the current maximum of the deque.
# The Deque basically tracks the current window. Appending and popping are each
# O(1) from a normal deque. From this one, popping is O(size_of_deque) because
# you might have to iterate over the deque to find a new maximum.
class SmartDeque():
    def __init__(self):
        self.size = 0
        self.deque = deque()
        self.total = 0
        self.maximum = 0

    def appendleft(self, x):
        self.deque.appendleft(x)
        self.size += 1
        self.total += x
        if x > self.maximum:
            self.maximum = x

    def pop(self):
        # I wasn't sure of behavior when using maxlen - would the append 
        # function return what was popped when maxlen was exceeded? The docs
        # didn't elaborate on this
        popped = self.deque.pop()
        self.size -= 1
        self.total -= popped
        
        if popped == self.maximum:
            # Find new maximum by iterating over deque
            self.maximum = -1
            counter = 0
            while counter < self.size:
                counter += 1
                toRotate = self.deque.pop()
                if toRotate > self.maximum:
                    self.maximum = toRotate
                self.deque.appendleft(toRotate)
        return popped

    def getSize(self):
        return self.size

    def __str__(self):
        return self.deque.__str__()

    def getTotal(self):
        return self.total

    def getMaximum(self):
        return self.maximum

# I started implementing using separate classes for Averages and Maximums to
# make things clearer for myself, but this class isn't used in the actual code.
# I would have deleted it in real code, but wanted to leave it here to show
# my thoughts as I was working through the problem.
class AveragesDeque():

    def __init__(self):
        self.size = 0
        self.deque = deque()
        self.total = 0

    def appendleft(self, x):
        self.deque.appendleft(x)
        self.size += 1
        self.total += x

    def pop(self):
        # I wasn't sure of behavior when using maxlen - would the append 
        # function return what was popped when maxlen was exceeded? The docs
        # didn't elaborate on this
        popped = self.deque.pop()
        self.size -= 1
        self.total -= popped
        return popped

    def getSize(self):
        return self.size

    def __str__(self):
        return self.deque.__str__()

    def getTotal(self):
        return self.total

# I started implementing using separate classes for Averages and Maximums to
# make things clearer for myself, but this class isn't used in the actual code.
# I would have deleted it in real code, but wanted to leave it here to show
# my thoughts as I was working through the problem.
class MaximumsDeque():
    def __init__(self):
        self.size = 0
        self.deque = deque()
        self.maximum = 0

    def appendleft(self, x):
        self.deque.appendleft(x)
        self.size += 1
        if x > self.maximum:
            self.maximum = x

    def pop(self):
        popped = self.deque.pop()
        self.size -= 1
        if popped == self.maximum:
            # Find new maximum by iterating over deque
            self.maximum = -1
            counter = 0
            while counter < self.size:
                counter += 1
                toRotate = self.deque.pop()
                if toRotate > self.maximum:
                    self.maximum = toRotate
                self.deque.appendleft(toRotate)
        return popped

    def getSize(self):
        return self.size

    def __str__(self):
        return self.deque.__str__()

    def getMaximum(self):
        return self.maximum

class WindowGenerator:

    def __init__(self, streamIterator):
        self.streamIterator = streamIterator

    # This function calculates the average and the maximum for the data stored
    # in the supporting SmartDeque.
    def doBoth(self, smartDeque, window, item):
        toReturn = (None, None)
        smartDeque.appendleft(item)
        # I've commented out my debugging statement for submission.
        #print smartDeque, smartDeque.getTotal(), smartDeque.getMaximum()
        if smartDeque.getSize() == window:
            # Calculate the average using the deque's stored total and size
            average = smartDeque.getTotal() / smartDeque.getSize()
            # Grab the maximum
            maximum = smartDeque.getMaximum()
            smartDeque.pop()
            toReturn = (average, maximum)
        return toReturn

    # I eventually compressed this function into doBoth, but originally had this
    # and doMaximum separately to help me get started.
    def doAverage(self, averagesDeque, window, item):
        toReturn = None
        averagesDeque.appendleft(item)
        print averagesDeque, averagesDeque.getTotal()
        if averagesDeque.getSize() == window:
            toReturn = averagesDeque.getTotal() / averagesDeque.getSize()
            averagesDeque.pop()
        return toReturn

    # I eventually compressed this function into doBoth.
    def doMaximum(self, maximumsDeque, window, item):
        toReturn = None
        maximumsDeque.appendleft(item)
        print maximumsDeque, maximumsDeque.getMaximum()
        if maximumsDeque.getSize() == window:
            toReturn = maximumsDeque.getMaximum()
            maximumsDeque.pop()
        return toReturn

    def generate(self, window1, window2):
        #deque1 = AveragesDeque()
        #deque2 = AveragesDeque()
        #maxDeque1 = MaximumsDeque()
        #maxDeque2 = MaximumsDeque()
        deque1 = SmartDeque()
        deque2 = SmartDeque()

        for item in self.streamIterator:
            print self.doBoth(deque1, window1, item) + self.doBoth(deque2, window2, item)
            #average1 = self.doAverage(deque1, window1, item)
            #average2 = self.doAverage(deque2, window2, item)
            #maximum1 = self.doMaximum(maxDeque1, window1, item)
            #maximum2 = self.doMaximum(maxDeque2, window2, item)
            #print (average1, maximum1, average2, maximum2)

if __name__ == '__main__':
    generator = WindowGenerator(iter([1, 2, 3, 4, 5, 6]))
    #generator.generate(3, 5)
    generator.generate(3, 20)
    generator = WindowGenerator(iter([6, 5, 4, 3, 2, 1]))
    #generator.generate(3, 5)
    generator.generate(3, 20)
    pass
