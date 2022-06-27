def fillNumber(imgt, point):
    dirct = [-1, -1, -1, 0, -1, 1, 0, -1, 0, 1, 1, -1, 1, 0, 1, 1]
    h = len(imgt)
    w = len(imgt[0])
    q = [point]
    side = [i for i in point for j in range(2)]
    while len(q) != 0:
        t = q.pop()
        if imgt[t[0]][t[1]] == 0:
            continue
        imgt[t[0]][t[1]] = 0
        if t[0] < side[0]:
            side[0] = t[0]
        elif t[0] > side[1]:
            side[1] = t[0]
        if t[1] < side[2]:
            side[2] = t[1]
        elif t[1] > side[3]:
            side[3] = t[1]
        for i in range(8):
            x = t[0] + dirct[2 * i]
            y = t[1] + dirct[2 * i + 1]
            if imgt[x][y] != 0:
                q.append([x, y])
    if (side[1] - side[0]) * (side[3] - side[2]) < 1024:
        side = []
    if len(side) != 0:
        side[0] -= 1
        side[1] += 1
        side[2] -= 1
        side[3] += 1
    return side


def separateNumbers(img):
    h, w, c = img.shape
    step = w//150
    imgt = [[sum(img[i][j]) for j in range(w)] for i in range(h)]
    side = []
    for i in range(0, h, step):
        for j in range(0, w, step):
            if imgt[i][j] != 0:
                newside = fillNumber(imgt, [i, j])
                if len(newside) != 0:
                    side.append(newside)
    return side


def quickSeparateNumbers(img):
    h = len(img)
    w = len(img[0])
    step = w >> 8
    if step == 0:
        step = 1
    imgt = [[img[i][j] for j in range(0, w, step)] for i in range(0, h, step)]
    side = []
    newh = h // step
    neww = w // step
    for i in range(0, newh):
        for j in range(0, neww):
            if imgt[i][j] != 0:
                newside = fillNumber(imgt, [i, j])
                if len(newside) != 0:
                    side.append([i*step for i in newside])
    imgList = list()
    for each in side:
        imgList.append([[img[i][j] for j in range(each[2], each[3]+1)] for i in range(each[0], each[1]+1)])
    return imgList