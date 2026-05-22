
class Filter:

    # constructor
    def __init__(self, low_H = None, low_S = None, low_V = None, high_H = None, high_S = None, high_V = None, 
                 sub_S = None, sub_V = None, add_S = None, add_V = None):
        self.low_H = low_H
        self.low_S = low_S
        self.low_V = low_V
        self.high_H = high_H
        self.high_S = high_S
        self.high_V = high_V
        self.sub_S = sub_S 
        self.sub_V = sub_V 
        self.add_S = add_S
        self.add_V = add_V

