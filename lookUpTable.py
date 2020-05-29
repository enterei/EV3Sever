class LookUpTable:

    def lookUpField(self, idx):
        if (idx == 0):
            return [2, 0]
        if (idx == 1):
            return [2, 1]
        if (idx == 2):
            return [2, 2]
        if (idx == 3):
            return [1, 0]
        if (idx == 4):
            return [1, 1]
        if (idx == 5):
            return [1, 2]
        if (idx == 6):
            return [0, 0]
        if (idx == 7):
            return [0, 1]
        if (idx == 8):
            return [0, 2]

    def lookUpTable(self, idx):
        if idx[0] == 2 and idx[1] == 0:
            return 0
        if idx[0] == 2 and idx[1] == 1:
            return 1
        if idx[0] == 2 and idx[1] == 1:
            return 1
        if idx[0] == 2 and idx[1] == 2:
            return 2
        if idx[0] == 1 and idx[1] == 0:
            return 3
        if idx[0] == 1 and idx[1] == 1:
            return 4
        if idx[0] == 1 and idx[1] == 2:
            return 5
        if idx[0] == 0 and idx[1] == 0:
            return 6
        if idx[0] == 0 and idx[1] == 1:
            return 7
        if idx[0] == 0 and idx[1] == 2:
            return 8