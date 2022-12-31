import copy
from copy import deepcopy
import numpy as np


class GameField(object):
    def __init__(self):
        self.__field = np.zeros((3, 3), dtype=int)  # заполняем поле 3*3 нулями
        self.__F = 0  # значение функции G + H
        self.__G = 0  # кол-во фишек не на своих местах
        self.__H = -1  # номер хода
        self.__chooseNumber = 0  # номер выбранного поля по счету
        self.__id = 0  # id поля для дальнейшей сортировки
        self.__parentId = -1  # id поля, от которого был ход

    # поле
    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, array):
        self.__field = np.array(array)

    @property
    def F(self):
        return self.__F

    @F.setter
    def F(self, f):
        if 0 <= f:
            self.__F = f
        else:
            print("Некорректное значение")

    # кол-во фишек не на своих местах
    @property
    def G(self):
        return self.__G

    @G.setter
    def G(self, g):
        if 0 <= g <= 9:
            self.__G = g
            self.__F = self.__G + self.__H
        else:
            print("Некорректное значение")

    # номер хода
    @property
    def H(self):
        return self.__H

    @H.setter
    def H(self, h):
        if -1 <= h:
            self.__H = h
            self.__F = self.__G + self.__H
        else:
            print("Некорректное значение")

    # номер выбранного поля по счету
    @property
    def chooseNumber(self):
        return self.__chooseNumber

    @chooseNumber.setter
    def chooseNumber(self, chooseNumber):
        if 0 <= chooseNumber:
            self.__chooseNumber = chooseNumber
        else:
            print("Некорректное значение")

    # id поля для дальнейшей сортировки
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if 0 <= id:
            self.__id = id
        else:
            print("Некорректное значение")

    # id поля для дальнейшей сортировки
    @property
    def parentId(self):
        return self.__parentId

    @parentId.setter
    def parentId(self, parentId):
        if -1 <= parentId:
            self.__parentId = parentId
        else:
            print("Некорректное значение")

    # метод для отображения информации о игровом поле
    def DisplayInfo(self):
        for line in self.__field:
            print(*line)
        print(f"id: {self.__id}\nЛучший вариант: {self.__chooseNumber if self.__chooseNumber != 0 else 'не лучший'}\n"
              f"Количество фишек не на своих местах {self.__G} \nНомер хода {self.__H} \n"
              f"id родительского поля {self.__parentId}\n"
              f"--------------------------")


class Game:
    def __init__(self):
        self.__fields = []

    @property
    def fields(self):
        return self.__fields

    def CreateStartField(self, array):  # создание стартового игрового поля
        newField = GameField()
        newField.field = np.array(array)
        newField.chooseNumber = 1
        newField.id = len(self.__fields)
        self.__fields.append(newField)

    def CreateNewField(self, array, h, g, parentId):  # создание нового поля
        newField = GameField()
        newField.field = np.array(array)
        newField.G = g
        # newField.H = h
        if(h == 0):
            newField.H = h
        else:
            parent = list(filter(lambda field: field.id == parentId, self.__fields))
            parentH = parent[0].H
            newField.H = parentH + 1
        newField.parentId = parentId
        newField.id = len(self.__fields)
        self.__fields.append(newField)

    def ChooseFieldAsBest(self, field, value):  # метод выбора лучшего поля
        thisField = self.__fields[field.id]
        thisField.chooseNumber = value

    def DisplayInfo(self, field):  # отображение информации о поле
        thisField = self.__fields[field.id]
        thisField.DisplayInfo()

    def ChooseBestField(self, iterNumber):
        if len(self.__fields) == 1:
            thisField = self.__fields[0]
            thisField.chooseNumber = iterNumber
            return thisField
        else:
            filteredFields = list(filter(lambda field: field.chooseNumber == 0, self.__fields))
            sortedFields = sorted(filteredFields, key=lambda field: field.F, reverse=False)
            bestField = sortedFields[0]
            bestField.chooseNumber = iterNumber
            return bestField


    # def ChangeG(self, field, g):
    #     thisField = self.__fields[field.id]
    #     thisField.G = g


class Logic:
    @staticmethod
    def CalculateG(gameField):  # метод подсчета фишек не на своих местах
        goodMatrix = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        counter = 1
        g = 0
        for i in range(len(gameField.field)):
            for j in range(len(gameField.field[i])):
                if gameField.field[i][j] != goodMatrix[i][j]:
                    g += 1
        gameField.G = g  # записали значение G для поля

    @staticmethod
    def DisplayG(gameField):  # метод вывода G
        for line in gameField.field:
            print(*line)
        print(f"Фишек не на своих местах: {gameField.G}")

    @staticmethod
    def GeneratePossibleMoves(gameField):  # метод генерации возможных ходов
        fields = []
        thisField = copy.deepcopy(gameField.field)
        for i in range(len(thisField)):
            for j in range(len(thisField[i])):
                if thisField[i][j] == 0:
                    if i > 0:  # сверху есть фишка, можно передвинуть на пустое место
                        thisField[i][j] = thisField[i - 1][j]  # меняем местами с 0
                        thisField[i - 1][j] = 0
                        fields.append(thisField)  # добавляем в список возможных вариантов
                        thisField = copy.deepcopy(gameField.field)  # ставим старое значение

                    if j < 2:  # справа есть фишка, передвигаем
                        thisField[i][j] = thisField[i][j + 1]
                        thisField[i][j + 1] = 0
                        fields.append(thisField)
                        thisField = copy.deepcopy(gameField.field)

                    if i < 2:  # снизу есть фишка, переставляем
                        thisField[i][j] = thisField[i + 1][j]
                        thisField[i + 1][j] = 0
                        fields.append(thisField)
                        thisField = copy.deepcopy(gameField.field)

                    if j > 0:  # слева есть фишка, переставляем
                        thisField[i][j] = thisField[i][j - 1]
                        thisField[i][j - 1] = 0
                        fields.append(thisField)
                        thisField = copy.deepcopy(gameField.field)

        return fields
