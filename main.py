import cv2
import numpy


def openImg(name=""):
    orgimg = cv2.imread(r"res/pt4(1).jpg")
    assert orgimg is not None
    h, w = orgimg.shape[:2]
    img = [[0 if sum(orgimg[i][j]) < 50 else 1 for j in range(0, w)] for i in range(0, h)]
    return img


def dfa(img):
    h = len(img)
    w = len(img[0])
    startw = int(w * 0.45)
    p = [h - 1, startw]
    l, r = startw, startw
    while p[0] != 0:
        img[p[0]][p[1]] = 2
        p[0] -= 1
        value = img[p[0] - 1][p[1] - 1] * 10000 + img[p[0] - 1][p[1]] * 1000 + img[p[0] - 1][p[1] + 1] * 100 + \
                img[p[0]][p[1] - 1] * 10 + img[p[0]][p[1] + 1]
        if value == 11101:
            p[1] -= 2
        elif value == 1101:
            p[1] -= 1
        elif value == 11010:
            p[1] += 1
        elif value == 11110:
            p[1] += 2
        elif img[p[0]][p[1] - 1] == 1 and img[p[0]][p[1] + 1] == 1:
            p[1] -= 1
        if p[1] < l:
            l = p[1]
        elif p[1] > r:
            r = p[1]
    num1 = [[img[i][j] for j in range(r + 1)] for i in range(h)]
    num2 = [[img[i][j] for j in range(l - 1, w)] for i in range(h)]
    for i in range(h):
        for j in range(len(num1[0]) - 1, 0, -1):
            if num1[i][j] != 2:
                num1[i][j] = 0
            else:
                num1[i][j] = 0
                break
        for j in range(len(num2[0])):
            if num2[i][j] != 2:
                num2[i][j] = 0
            else:
                num2[i][j] = 0
                break
    numList = [num1, num2]
    for i in range(2):
        t = numList[i]
        numShape = [len(t), len(t[0])]
        t = [[0 if t[i][j] == 0 else 255 for j in range(numShape[1])] for i in range(numShape[0])]
        padding1 = numShape[0] - numShape[1]
        padding2 = padding1 // 2
        padding1 -= padding2
        for j in range(numShape[0]):
            t[j] = [0]*padding1 + t[j] + [0]*padding2
        t = numpy.array(t, numpy.uint8)
        numList[i] = t
    num1 = cv2.resize(numList[0], (28, 28), interpolation=cv2.INTER_AREA)
    num2 = cv2.resize(numList[1], (28, 28), interpolation=cv2.INTER_AREA)
    thresholding(num1)
    thresholding(num2)
    return [num1, num2]


def thresholding(img):
    h = len(img)
    w = len(img[0])
    for i in range(h):
        for j in range(w):
            if img[i][j] >= 20:
                img[i][j] = 255


if __name__ == '__main__':
    img = openImg("")
    numList = dfa(img)
    # 处理后结果比较糊，需要再做一遍二值，20为阈值
    cv2.imwrite(r"result/num1.jpg", numList[0])
    cv2.imwrite(r"result/num2.jpg", numList[1])
    print("DONE")
