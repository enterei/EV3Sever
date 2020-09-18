from random import randrange

v0 = [0, 1, 2] #win conditions
v1 = [3, 4, 5]
v2 = [6, 7, 8]

v3 = [0, 3, 6]
v4 = [1, 4, 7]
v5 = [2, 5, 8]

v6 = [0, 4, 8]
v7 = [6, 4, 2]


class GameHandler:
    field = []
    turn = 0   #todo change turn
    first = "E"

    stragity = None
    winner = None
    vcs = [v0, v1, v2, v3, v4, v5, v6, v7]  # Win Condition




    my_opportunity = []
    enemy_oppertunitiy = []


    def __init__(self, dM,kfirst="M", **kwargs):
        self.defaultMessage=dM
        self.first = kfirst
        self.vcs = [v0, v1, v2, v3, v4, v5, v6, v7] # possible active winconditions
        self.my_oppertunitiy = []
        self.enemy_oppertunitiy = []
        self.winner = None
        self.field = []
        self.game_on = True
        for i in range(9):
            self.field.append("N")  # neutral
        print("feld laenge: " + str(len(self.field)))
        if self.first == "M":  # me
            self.stragity = randrange(0, 2, 1)  # 1 = Middle, 2 = Corner


    def thinkMove(self, new_markedf_field_number):  # new
        my_option = self.checkOpportunity("M")
        if my_option != None:
            print("my option: " + str(my_option))
            return my_option
        enemy_option = self.checkOpportunity("E")
        if enemy_option != None:
            print("enemy option: " + str(enemy_option))
            return enemy_option
        if self.field[4]=="N":
            return 4
        corner_option = self.cornerOption()
        if corner_option !=None:
            return corner_option


        # if self.stragity != None:
        #   return self.getStragityMove() todo
        try_number = randrange(0, 8, 1)
        while self.field[try_number] != "N":
            try_number = randrange(0, 8, 1)
        print("random option: " + str(try_number))
        return try_number

        # return taret_field_number


    def getMove(self, new_marked_field_number):
        if new_marked_field_number != None:
            if not self.tagField(new_marked_field_number, "E"):  # enemy Move
                print("wrong move by: " + str("E"))
                self.wins("M")
                return False

        if self.checkEnd():  # check if game ended  Enemy Won?
            return False
        move = self.thinkMove(new_marked_field_number)
        if not self.tagField(move, "M"):  # my Move
            print("Wrong move by M")
            self.wins("E")
            return move
        if self.checkEnd():  # check if game ended I win
            return move

        return move


    def checkCondition(self, vc):
        target = self.field[vc[0]]
        if target =="N":
            return
        for i in vc:
            if self.field[i] != target:
                return None
        return target


    def checkEnd(self):
        if self.turn < 5:
            print("checkENd False")

            return False
        for i in self.vcs:
            if self.checkCondition(i):
                self.wins(self.field[i[0]])
                #self.game_on=False
                print("checkENd True")

                return True
        if self.turn==9:
            self.wins(None)

            return True
        print("checkENd False")

        return False


    def checkOpportunity(self, tagret):
        for i in self.vcs:
            if self.countVc(i, tagret) == 2:
                for target_idx in i:
                    if self.field[target_idx] == "N":
                        return target_idx
        return None


    def countVc(self, vc, target):
        counter = 0
        for i in vc:
            if self.field[i] == target:
                counter = counter + 1
        return counter


    def getStragityMove(self):
        return None


    def tagField(self, target_field, player):  #todo change turn
        print(player + " setzt " + str(target_field))
        print(int(target_field))

        if self.field[int(target_field)] != "N":
            return False
        self.field[int(target_field)] = player
        self.turn = self.turn + 1  # danach (vielleich nocht wichtig)
        self.print()

        return True


    def wins(self, player):
        self.winner = player
        self.game_on = False
        print(player + " has won the game")
        print("End Table:")
        self.print()


    def print(self):
        print(self.field[0] + "  " + self.field[1] + "  " + self.field[2])
        print(self.field[3] + "  " + self.field[4] + "  " + self.field[5])
        print(self.field[6] + "  " + self.field[7] + "  " + self.field[8])


    def getWinner(self):
        return self.winner


    def getNeutral(self):
        res = []
        newres=[]
        for i in range(9):
           # print(i)
            if self.field[i] == "N":
                res.append(i)


        if 0 in res:
            newres.append(0)
        if 1 in res:
            newres.append(1)
        if 2 in res:
            newres.append(2)

        if 5 in res:
            newres.append(5)
        if 4 in res:
            newres.append(4)
        if 3 in res:
            newres.append(3)
        if 6 in res:
            newres.append(6)

        if 7 in res:
            newres.append(7)
        if 8 in res:
            newres.append(8)


        print(newres)
        return newres
    def cornerOption(self):
        neutral_corners=[]
        if self.field[0]=="N":
            neutral_corners.append(0)
        if self.field[2]=="N":
            neutral_corners.append(2)
        if self.field[6]=="N":
            neutral_corners.append(6)
        if self.field[0]=="N":
            neutral_corners.append(8)
        idx = randrange(0, len(neutral_corners),1)
        return neutral_corners[idx]



def main(): #main for testing gamelogic and KI without hte robot
    dm="ga"

    game = GameHandler(kfirst="E4",dM="ga")
    game.print()
    bc = True
    if game.turn == 0 and game.first == "M":
        bc = game.getMove(None)
    while bc:
        value = input("Setz Spielzug nummber: " + str(game.turn))
        print(value)
        bc = game.getMove(int(value))
        print(bc)
        print(game.getNeutral())


if __name__ == '__main__':
    # server()
    main()
