#! /usr/bin/env python3

"""Overview:
2048 self-solve problem.
実行例：py -3 2048.py -auto_mode 3 -print_mode 1 -one_time 1 -seed 5
2017/12/31 Go言語版からPython3版に移植開始
2019/01/14 Python3で動き始める（バグあり）
2019/01/19 Python3に移植完了
2019/02/09 パラメータ対応(docopt, argparse)

PEP8準拠チェック：
py.test --pep8 xxxxxxxx.py

Usage:
  2048 [-auto_mode <auto_mode>]
       [-calc_gap_mode <calc_gap_mode>]
       [-print_mode <print_mode>]
       [-print_mode_turbo <print_mode_turbo>]
       [-pause_mode <pause_mode>]
       [-turbo_minus <turbo_minus>]
       [-turbo_minus_percent <turbo_minus_percent>]
       [-turbo_minus_percent_level <turbo_minus_percent_level>]
       [-turbo_minus_score <turbo_minus_score>]
       [-turbo_minus_score_level <turbo_minus_score_level>]
       [-turbo_plus_percent <turbo_plus_percent>]
       [-turbo_plus_percent_level <turbo_plus_percent_level>]
       [-turbo_plus_score <turbo_plus_score>]
       [-turbo_plus_score_level <turbo_plus_score_level>]
       [-one_time <one_time>]
       [-seed <seed>]

Options:
  -auto_mode                 : 任意オプション(引数あり)
  -calc_gap_mode             : 任意オプション(引数あり)
  -print_mode                : 任意オプション(引数あり)
  -print_mode_turbo          : 任意オプション(引数あり)
  -pause_mode                : 任意オプション(引数あり)
  -turbo_minus               : 任意オプション(引数あり)
  -turbo_minus_percent       : 任意オプション(引数あり)
  -turbo_minus_percent_level : 任意オプション(引数あり)
  -turbo_minus_score         : 任意オプション(引数あり)
  -turbo_minus_score_level   : 任意オプション(引数あり)
  -turbo_plus_percent        : 任意オプション(引数あり)
  -turbo_plus_percent_level  : 任意オプション(引数あり)
  -turbo_plus_score          : 任意オプション(引数あり)
  -turbo_plus_score_level    : 任意オプション(引数あり)
  -one_time                  : 任意オプション(引数あり)
  -seed                      : 任意オプション(引数あり)

    args = docopt(__doc__)
    for k,v in args.items():
        if (k == "auto_mode"):
            auto_mode = v
        if (k == "calc_gap_mode"):
            calc_gap_mode = v
        if (k == "print_mode"):
            print_mode = v
        if (k == "print_mode_turbo"):
            print_mode_turbo = v
        if (k == "seed"):
            seed = v
        if (k == "one_time"):
            one_time = v
        if (k == "turbo_minus_percent"):
            turbo_minus_percent = v
        if (k == "turbo_minus_percent_level"):
            turbo_minus_percent_level = v
        if (k == "turbo_minus_score"):
            turbo_minus_score = v
        if (k == "turbo_minus_score_level"):
            turbo_minus_score_level = v
        if (k == "turbo_plus_percent"):
            turbo_plus_percent = v
        if (k == "turbo_plus_percent_level"):
            turbo_plus_percent_level = v
        if (k == "turbo_plus_score"):
            turbo_plus_score = v
        if (k == "turbo_plus_score_level"):
            turbo_plus_score_level = v
"""

import sys
import random as rand
import time
#from docopt import docopt # Windows版には入っていない？
import argparse # Python標準らしい

auto_mode = 4 # >=0 depth
calc_gap_mode = 0 # 0:normal 1:端が小さい+1 2:*2 3:+大きい値 4:+大きい値/10 5:+両方
print_mode = 100 # 途中経過の表示間隔(0：表示しない)
print_mode_turbo = 1
pause_mode = 0
turbo_minus_percent       = 55
turbo_minus_percent_level = 1
turbo_minus_score         = 20000
turbo_minus_score_level   = 1
turbo_plus_percent        = 10
turbo_plus_percent_level  = 1
turbo_plus_score          = 200000
turbo_plus_score_level    = 1
one_time = 1 # 繰り返し回数
seed = 1

D_BONUS = 10
D_BONUS_USE_MAX = True  # 10固定ではなく最大値とする
GAP_EQUAL = 0

INIT2 = 1
INIT4 = 2
RNDMAX = 4
GAP_MAX = 100000000.0
XMAX = 4
YMAX = 4
XMAX_1 = (XMAX-1)
YMAX_1 = (YMAX-1)


def make_array(x, y, v=0):
    return [[v for i in range(x)] for j in range(y)]

board = make_array(XMAX, YMAX)
sp = 0

pos_x = list(range(XMAX*YMAX))
pos_y = list(range(XMAX*YMAX))
pos_val = list(range(XMAX*YMAX))
qscore = 0
gen = 0
count_2 = 0
count_4 = 0
count_calcGap = 0
count_getGap = 0

start_time = 0
last_time = 0
total_start_time = 0
total_last_time = 0
count = 0
sum_score = 0
max_score = 0
max_seed = 0
min_score = (GAP_MAX)
min_seed = 0
ticks_per_sec = 1


def main():
    global seed, gen, count, sum_score
    global max_score, max_seed, min_score, min_seed, one_time, total_last_time
    global auto_mode, calc_gap_mode, print_mode, print_mode_turbo
    global pause_mode, seed, one_time
    global turbo_minus_percent, turbo_minus_percent_level
    global turbo_minus_score, turbo_minus_score_level
    global turbo_plus_percent, turbo_plus_percent_level
    global turbo_plus_score, turbo_plus_score_level

    parser = argparse.ArgumentParser(description='2048 self-solve problem.')
    parser.add_argument('-auto_mode', default=auto_mode, type=int)
    parser.add_argument('-calc_gap_mode', default=calc_gap_mode, type=int)
    parser.add_argument('-print_mode', default=print_mode, type=int)
    parser.add_argument('-print_mode_turbo', default=print_mode_turbo, type=int)
    parser.add_argument('-pause_mode', default=pause_mode, type=int)
    parser.add_argument('-seed', default=seed, type=int)
    parser.add_argument('-one_time', default=one_time, type=int)
    parser.add_argument('-turbo_minus_percent', default=turbo_minus_percent, type=int)
    parser.add_argument('-turbo_minus_percent_level', default=turbo_minus_percent_level, type=int)
    parser.add_argument('-turbo_minus_score', default=turbo_minus_score, type=int)
    parser.add_argument('-turbo_minus_score_level', default=turbo_minus_score_level, type=int)
    parser.add_argument('-turbo_plus_percent', default=turbo_plus_percent, type=int)
    parser.add_argument('-turbo_plus_percent_level', default=turbo_plus_percent_level, type=int)
    parser.add_argument('-turbo_plus_score', default=turbo_plus_score, type=int)
    parser.add_argument('-turbo_plus_score_level', default=turbo_plus_score_level, type=int)
    args = parser.parse_args()
    auto_mode = args.auto_mode
    calc_gap_mode = args.calc_gap_mode
    print_mode = args.print_mode
    print_mode_turbo = args.print_mode_turbo
    pause_mode = args.pause_mode
    seed = args.seed
    one_time = args.one_time
    turbo_minus_percent = args.turbo_minus_percent
    turbo_minus_percent_level = args.turbo_minus_percent_level
    turbo_minus_score = args.turbo_minus_score
    turbo_minus_score_level = args.turbo_minus_score_level
    turbo_plus_percent = args.turbo_plus_percent
    turbo_plus_percent_level = args.turbo_plus_percent_level
    turbo_plus_score = args.turbo_plus_score
    turbo_plus_score_level = args.turbo_plus_score_level

    print("auto_mode={}".format(auto_mode))
    print("calc_gap_mode={}".format(calc_gap_mode))
    print("print_mode={}".format(print_mode))
    print("print_mode_turbo={}".format(print_mode_turbo))
    print("pause_mode={}".format(pause_mode))
    print("seed={}".format(seed))
    print("one_time={}".format(one_time))
    print("turbo_minus_percent={}".format(turbo_minus_percent))
    print("turbo_minus_percent_level={}".format(turbo_minus_percent_level))
    print("turbo_minus_score={}".format(turbo_minus_score))
    print("turbo_minus_score_level={}".format(turbo_minus_score_level))
    print("turbo_plus_percent={}".format(turbo_plus_percent))
    print("turbo_plus_percent_level={}".format(turbo_plus_percent_level))
    print("turbo_plus_score={}".format(turbo_plus_score))
    print("turbo_plus_score_level={}".format(turbo_plus_score_level))
	
    if (seed > 0):
        rand.seed(seed)
    else:
        rand.seed(time.time() * 1000000)
    total_start_time = time.time()
    init_game()
    count += 1
    while True:
        gap = moveAuto(auto_mode)
        gen += 1
        appear()
        disp(gap, print_mode > 0 and (
            gen % print_mode == 0 or (
                print_mode_turbo == 1 and score > turbo_minus_score
                ) or (
                print_mode_turbo == 2 and score > turbo_plus_score)))
        if (isGameOver()):
            sc = getScore()
            sum_score += sc
            if (sc > max_score):
                max_score = sc
                max_seed = seed
            if (sc < min_score):
                min_score = sc
                min_seed = seed
            print("Game Over! (level={} seed={}) {} #{} Ave.={}".format(
                auto_mode, seed, getTime(), count, sum_score/count), end=" ")
            print("Max={}(seed={}) Min={}(seed={})".format(
                max_score, max_seed, min_score, min_seed))
            print("getGap={} calcGap={} {:.1f},{:.1f}".format(
                count_getGap, count_calcGap, D_BONUS, (GAP_EQUAL)), end=" ")
            print("{}%,{} {},{} {}%,{} {},{} {} calc_gap_mode={}".format(
                turbo_minus_percent, turbo_minus_percent_level,
                turbo_minus_score, turbo_minus_score_level,
                turbo_plus_percent, turbo_plus_percent_level,
                turbo_plus_score, turbo_plus_score_level,
                print_mode_turbo, calc_gap_mode))
            disp(gap, True)
            if (one_time > 0):
                one_time -= 1
                if (one_time == 0):
                    break
            if (pause_mode > 0):
                key = input('q=quit ')
                if (key == "q"):
                    break
            seed += 1
            rand.seed(seed)
            init_game()
            count += 1
    total_last_time = time.time()
    print("Total time = {:.1f} (sec)".format(
        (total_last_time-total_start_time)/ticks_per_sec))


def disp(gap, debug):
    global last_time
    now = time.time()
    print("[{}:{}] {} ({:.2f}/{:.1f} sec) {:.6f} {} seed={} 2={:.2f}%".format(
        count, gen, getScore(), (now-last_time), (now-start_time), gap,
        getTime(), seed, (count_2)/(count_2+count_4)*100), end='')
    if count == 0:
        print("\r", end='')
    else:
        print(" Ave.={}\r".format((sum_score+getScore())/count), end='')
    last_time = now
    if debug:
        print()
        for y in range(YMAX):
            for x in range(XMAX):
                v = getCell(x, y)
                print("{:>5}".format((1 << v) if v > 0 else "."), end=' ')
            print()


def getCell(x, y):
    return (board[x][y])


def setCell(x, y, n):
    board[x][y] = (n)
    return (n)


def clearCell(x, y):
    (setCell(x, y, 0))


def copyCell(x1, y1, x2, y2):
    return (setCell(x2, y2, getCell(x1, y1)))


def moveCell(x1, y1, x2, y2):
    copyCell(x1, y1, x2, y2)
    clearCell(x1, y1)


def addCell(x1, y1, x2, y2):
    board[x2][y2] += 1
    clearCell(x1, y1)
    if (sp < 1):
        addScore(1 << (getCell(x2, y2)))


def isEmpty(x, y):
    return (getCell(x, y) == 0)


def isNotEmpty(x, y):
    return (not isEmpty(x, y))


def isGameOver():
    ret, _, _ = isMovable()
    if ret:
        return False
    else:
        return True


def getScore():
    return (score)


def setScore(sc):
    global score
    score = (sc)
    return (score)


def addScore(sc):
    global score
    score += (sc)
    return score


def clear():
    for y in range(YMAX):
        for x in range(XMAX):
            clearCell(x, y)


def init_game():
    global gen, start_time, last_time
    global count_2, count_4, count_calcGap, count_getGap
    gen = 1
    setScore(0)
    start_time = time.time()
    last_time = start_time
    count_2 = 0
    count_4 = 0
    count_calcGap = 0
    count_getGap = 0
    clear()
    appear()
    disp(0.0, print_mode == 1)


def getTime():
    return time.strftime("%Y/%m/%d %H:%M:%S")


def appear():
    global count_2, count_4
    n = 0
    for y in range(YMAX):
        for x in range(XMAX):
            if (isEmpty(x, y)):
                pos_x[n] = x
                pos_y[n] = y
                n += 1
    if (n > 0):
        i = rand.randint(0, 65535) % n
        if ((rand.randint(0, 65535) % RNDMAX) >= 1):
            v = INIT2
            count_2 += 1
        else:
            v = INIT4
            count_4 += 1
        x = pos_x[i]
        y = pos_y[i]
        setCell(x, y, v)
        return True
    return False


def countEmpty():
    ret = 0
    for y in range(YMAX):
        for x in range(XMAX):
            if (isEmpty(x, y)):
                ret += 1
    return ret


def move_up():
    move = 0
    for x in range(XMAX):
        yLimit = 0
        for y in range(1, YMAX):
            if (isNotEmpty(x, y)):
                yNext = y - 1
                while yNext >= yLimit:
                    if (isNotEmpty(x, yNext)):
                        break
                    if (yNext == 0):
                        break
                    yNext = yNext - 1
                if (yNext < yLimit):
                    yNext = yLimit
                if (isEmpty(x, yNext)):
                    moveCell(x, y, x, yNext)
                    move += 1
                else:
                    if (getCell(x, yNext) == getCell(x, y)):
                        addCell(x, y, x, yNext)
                        move += 1
                        yLimit = yNext + 1
                    else:
                        if (yNext+1 != y):
                            moveCell(x, y, x, yNext+1)
                            move += 1
                            yLimit = yNext + 1
    return move


def move_left():
    move = 0
    for y in range(YMAX):
        xLimit = 0
        for x in range(1, XMAX):
            if (isNotEmpty(x, y)):
                xNext = x - 1
                while xNext >= xLimit:
                    if (isNotEmpty(xNext, y)):
                        break
                    if (xNext == 0):
                        break
                    xNext = xNext - 1
                if (xNext < xLimit):
                    xNext = xLimit
                if (isEmpty(xNext, y)):
                    moveCell(x, y, xNext, y)
                    move += 1
                else:
                    if (getCell(xNext, y) == getCell(x, y)):
                        addCell(x, y, xNext, y)
                        move += 1
                        xLimit = xNext + 1
                    else:
                        if (xNext+1 != x):
                            moveCell(x, y, xNext+1, y)
                            move += 1
                            xLimit = xNext + 1
    return move


def move_down():
    move = 0
    for x in range(XMAX):
        yLimit = YMAX_1
        for y in range(YMAX - 2, -1, -1):
            if (isNotEmpty(x, y)):
                yNext = y + 1
                while yNext <= yLimit:
                    if (isNotEmpty(x, yNext)):
                        break
                    if (yNext == YMAX_1):
                        break
                    yNext = yNext + 1
                if (yNext > yLimit):
                    yNext = yLimit
                if (isEmpty(x, yNext)):
                    moveCell(x, y, x, yNext)
                    move += 1
                else:
                    if (getCell(x, yNext) == getCell(x, y)):
                        addCell(x, y, x, yNext)
                        move += 1
                        yLimit = yNext - 1
                    else:
                        if (yNext-1 != y):
                            moveCell(x, y, x, yNext-1)
                            move += 1
                            yLimit = yNext - 1
    return move


def move_right():
    move = 0
    for y in range(YMAX):
        xLimit = XMAX_1
        for x in range(XMAX - 2, -1, -1):
            if (isNotEmpty(x, y)):
                xNext = x + 1
                while xNext <= xLimit:
                    if (isNotEmpty(xNext, y)):
                        break
                    if (xNext == XMAX_1):
                        break
                    xNext = xNext + 1
                if (xNext > xLimit):
                    xNext = xLimit
                if (isEmpty(xNext, y)):
                    moveCell(x, y, xNext, y)
                    move += 1
                else:
                    if (getCell(xNext, y) == getCell(x, y)):
                        addCell(x, y, xNext, y)
                        move += 1
                        xLimit = xNext - 1
                    else:
                        if (xNext-1 != x):
                            moveCell(x, y, xNext-1, y)
                            move += 1
                            xLimit = xNext - 1
    return move


def moveAuto(autoMode):
    empty = countEmpty()
    sc = getScore()
    if (empty >= XMAX*YMAX*turbo_minus_percent/100):
        autoMode -= turbo_minus_percent_level
    elif (empty < XMAX*YMAX*turbo_plus_percent/100):
        autoMode += turbo_plus_percent_level
    if (sc < turbo_minus_score):
        autoMode -= turbo_minus_score_level
    elif (sc >= turbo_plus_score):
        autoMode += turbo_plus_score_level
    return moveBest(autoMode, True)


def moveBest(nAutoMode, move):
    global sp
    nDirBest = 0
    nDir = 0
    board_bak = make_array(XMAX, YMAX)
    copyBoard(board, board_bak)
    sp += 1
    nGapBest = GAP_MAX
    if (move_up() > 0):
        nDir = 1
        nGap = getGap(nAutoMode, nGapBest)
        if (nGap < nGapBest):
            nGapBest = nGap
            nDirBest = 1
    copyBoard(board_bak, board)
    if (move_left() > 0):
        nDir = 2
        nGap = getGap(nAutoMode, nGapBest)
        if (nGap < nGapBest):
            nGapBest = nGap
            nDirBest = 2
    copyBoard(board_bak, board)
    if (move_down() > 0):
        nDir = 3
        nGap = getGap(nAutoMode, nGapBest)
        if (nGap < nGapBest):
            nGapBest = nGap
            nDirBest = 3
    copyBoard(board_bak, board)
    if (move_right() > 0):
        nDir = 4
        nGap = getGap(nAutoMode, nGapBest)
        if (nGap < nGapBest):
            nGapBest = nGap
            nDirBest = 4
    copyBoard(board_bak, board)
    sp -= 1
    if (move):
        if (nDirBest == 0):
            print("***** Give UP *****")
            nDirBest = nDir
        if nDirBest == 1:
            move_up()
        elif nDirBest == 2:
            move_left()
        elif nDirBest == 3:
            move_down()
        elif nDirBest == 4:
            move_right()
    return nGapBest


def copyBoard(a, b):
    for y in range(YMAX):
        for x in range(XMAX):
            b[x][y] = a[x][y]


def getGap(nAutoMode, nGapBest):
    global count_getGap
    count_getGap += 1
    ret = 0.0
    movable, nEmpty, nBonus = isMovable()
    if (not movable):
        ret = GAP_MAX
    elif (nAutoMode <= 1):
        ret = getGap1(nGapBest, nEmpty, nBonus)
    else:
        alpha = nGapBest * (nEmpty)  # 累積がこれを超えれば、平均してもnGapBestを超えるので即枝刈りする
        for x in range(XMAX):
            for y in range(YMAX):
                if (isEmpty(x, y)):
                    setCell(x, y, INIT2)
                    ret += moveBest(nAutoMode-1, False) * (RNDMAX - 1) / RNDMAX
                    if (ret >= alpha):
                        return GAP_MAX  # 枝刈り
                    setCell(x, y, INIT4)
                    ret += moveBest(nAutoMode-1, False) / RNDMAX
                    if (ret >= alpha):
                        return GAP_MAX  # 枝刈り
                    clearCell(x, y)
        ret /= (nEmpty)  # 平均値を返す
    return ret


def getGap1(nGapBest, nEmpty, nBonus):
    ret = 0.0
    ret_appear = 0.0
    alpha = nGapBest * nBonus
    edgea = False
    edgeb = False
    R_3_4 = 1.0 * (RNDMAX - 1) / RNDMAX
    for x in range(XMAX):
        for y in range(YMAX):
            v = getCell(x, y)
            edgea = (x == 0 or y == 0) or (x == XMAX_1 or y == YMAX_1)
            if (v > 0):
                if (x < XMAX_1):
                    x1 = getCell(x+1, y)
                    edgeb = (y == 0) or (x + 1 == XMAX_1 or y == YMAX_1)
                    if (x1 > 0):
                        ret += calcGap(v, x1, edgea, edgeb)
                    else:
                        ret_appear += calcGap(v, INIT2, edgea, edgeb) * R_3_4
                        ret_appear += calcGap(v, INIT4, edgea, edgeb) / RNDMAX
                if (y < YMAX_1):
                    y1 = getCell(x, y+1)
                    edgeb = (x == 0) or (x == XMAX_1 or y+1 == YMAX_1)
                    if (y1 > 0):
                        ret += calcGap(v, y1, edgea, edgeb)
                    else:
                        ret_appear += calcGap(v, INIT2, edgea, edgeb) * R_3_4
                        ret_appear += calcGap(v, INIT4, edgea, edgeb) / RNDMAX
            else:
                if (x < XMAX_1):
                    x1 = getCell(x+1, y)
                    edgeb = (y == 0) or (x+1 == XMAX_1 or y == YMAX_1)
                    if (x1 > 0):
                        ret_appear += calcGap(INIT2, x1, edgea, edgeb) * R_3_4
                        ret_appear += calcGap(INIT4, x1, edgea, edgeb) / RNDMAX
                if (y < YMAX_1):
                    y1 = getCell(x, y+1)
                    edgeb = (x == 0) or (x == XMAX_1 or y+1 == YMAX_1)
                    if (y1 > 0):
                        ret_appear += calcGap(INIT2, y1, edgea, edgeb) * R_3_4
                        ret_appear += calcGap(INIT4, y1, edgea, edgeb) / RNDMAX
            if (ret + ret_appear/(nEmpty) > alpha):
                return GAP_MAX
    ret += ret_appear / (nEmpty)
    ret /= nBonus
    return ret


def calcGap(a, b, edgea, edgeb):
    global count_calcGap
    count_calcGap += 1
    ret = 0
    if (a > b):
        ret = (a - b)
        if (calc_gap_mode > 0 and not edgea and edgeb):
            if calc_gap_mode == 1:
                ret += 1
            elif calc_gap_mode == 2:
                ret *= 2
            elif calc_gap_mode == 3:
                ret += (a)
            elif calc_gap_mode == 4:
                ret += (a) / 10
            elif calc_gap_mode == 5:
                ret += (a + b)
    elif (a < b):
        ret = (b - a)
        if (calc_gap_mode > 0 and edgea and not edgeb):
            if calc_gap_mode == 1:
                ret += 1
            elif calc_gap_mode == 2:
                ret *= 2
            elif calc_gap_mode == 3:
                ret += (b)
            elif calc_gap_mode == 4:
                ret += (b) / 10
            elif calc_gap_mode == 5:
                ret += (a + b)
    else:
        ret = GAP_EQUAL
    return ret


def isMovable() -> (bool, int, float):
    ret = False   # 動けるか？
    nEmpty = 0    # 空きの数
    nBonus = 1.0  # ボーナス（隅が最大値ならD_BONUS）
    max_x = 0
    max_y = 0
    max = 0
    for y in range(YMAX):
        for x in range(XMAX):
            val = getCell(x, y)
            if (val == 0):
                ret = True
                nEmpty += 1
            else:
                if (val > max):
                    max = val
                    max_x = x
                    max_y = y
                if (not ret):
                    if (x < XMAX_1):
                        x1 = getCell(x+1, y)
                        if (val == x1 or x1 == 0):
                            ret = True
                    if (y < YMAX_1):
                        y1 = getCell(x, y+1)
                        if (val == y1 or y1 == 0):
                            ret = True
    if (
        (max_x == 0 or max_x == XMAX_1) and
            (max_y == 0 or max_y == YMAX_1)):
        if (D_BONUS_USE_MAX):
            nBonus = (max)
        else:
            nBonus = D_BONUS
    return ret, nEmpty, nBonus

if __name__ == "__main__":
    main()
