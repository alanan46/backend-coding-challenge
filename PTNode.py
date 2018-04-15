class PTNode(object):
    def __init__(self, key=None, data=None):
        self.key = key
        self.data = data
        self.children = []
        self.isEnd = False
