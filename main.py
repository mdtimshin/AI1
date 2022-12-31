from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
from Game import Game, Logic


def gameOver():
    print('GAME OVER')

# создаем игру
newGame = Game()
# newGame.CreateStartField([[2, 4, 3], [1, 8, 5], [7, 0, 6]])
newGame.CreateStartField([[5, 7, 2], [1, 4, 8], [6, 3, 0]])
newGame.fields[0].H = 1000000000
# newGame.DisplayInfo(newGame.fields[0])

# считаем фишки не на своих местах
# Logic.CalculateG(newGame.fields[0])
# Logic.DisplayG(newGame.fields[0])

# генерация возможных ходов
# moves = Logic.GeneratePossibleMoves(newGame.fields[0])
# moves = np.array(moves)
# print(moves)

# создание поля для каждого из вариантов
# for move in moves:
#     Game.CreateNewField(newGame, move, 0, 0, 0)

# for field in newGame.fields:
#     Logic.CalculateG(field)
#     newGame.DisplayInfo(field)

# print('*************SECOND*****ITERATION**************')

# bestField = newGame.ChooseBestField(2)
# # bestField.DisplayInfo()
# moves = Logic.GeneratePossibleMoves(bestField)
# moves = np.array(moves)

# for move in moves:
#     Game.CreateNewField(newGame, move, 1, 0, bestField.id)


# for field in newGame.fields:
#     Logic.CalculateG(field)
#     newGame.DisplayInfo(field)

iterCounter = 0
goodMatrix = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
while True:
    # for field in newGame.fields:
    #     fieldList = field.field.tolist()
    #     if(fieldList == goodMatrix):
    #         gameOver()
    # подсчитываем кол-во неправильно расставленных фишек
    for field in newGame.fields:
        Logic.CalculateG(field)

    # находим лучшее поле
    bestField = newGame.ChooseBestField(iterCounter+1)

    # если все фишки на местах -> заканчиваем игру
    if bestField.G == 0:
        print(f'ВСЕГО ПОЛЕЙ ПРОСЧИТАНО = {len(newGame.fields)}')
        bestField.DisplayInfo()
        print(f'Эффективность = {round((bestField.H+2)*100/len(newGame.fields), 2)} %')
        optimalTrajectory = []
        optimalTrajectory.append(bestField)
        parent = list(filter(lambda field: field.id == bestField.parentId, newGame.fields))[0]
        while True:
            if (parent.id == 0):
                break
            optimalTrajectory.append(parent)
            parent = list(filter(lambda field: field.id == parent.parentId, newGame.fields))[0]
        optimalTrajectory.append(newGame.fields[0])
        optimalTrajectory.reverse()
        print(f'ВСЕГО ХОДОВ ДО ВЫИГРЫША = {len(optimalTrajectory)}')
        print(f'**************************************************'
              f'ОПТИМАЛЬНАЯ ТРАЕКТОРИЯ'
              f'**************************************************')
        for field in optimalTrajectory:
            field.DisplayInfo()
        arrayG = list(map(lambda field: field.G, optimalTrajectory))
        arrayN = list(map(lambda field: field.H + 1, optimalTrajectory))
        arrayN[0] = 0
        plt.plot(arrayN, arrayG)
        plt.xlabel('Номер решения')
        plt.ylabel('Кол-во фишек не на местах')
        plt.show()
        break

    # генерируем возможные ходы относительно лучшего поля
    moves = Logic.GeneratePossibleMoves(bestField)

    # удаление хода, который соответсвует предшествующему
    parentGrid = newGame.fields[0]
    parentId = bestField.parentId
    if parentId != -1:
        parentGrid = next((x for x in newGame.fields if x.id == parentId), None)
    movesGrid = np.array(moves)
    movesGridList = movesGrid.tolist()

    for move in movesGrid:
        if np.array_equal(move, parentGrid.field):
            moveList = move.tolist()
            movesGridList.remove(moveList)

    # добавление созданных полей в игру
    for move in movesGridList:
        Game.CreateNewField(newGame, move, iterCounter, 0, bestField.id)

    # следующий ход
    iterCounter += 1







