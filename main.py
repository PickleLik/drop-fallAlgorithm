import cv2
import numpy


def openImg(name=""):
    orgimg = cv2.imread(r"res/p4.jpg")
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
        value = img[p[0]-1][p[1]-1]*10000 + img[p[0]-1][p[1]]*1000 + img[p[0]-1][p[1]+1]*100 +\
                img[p[0]][p[1]-1]*10 + img[p[0]][p[1]+1]
        if value == 11101:
            p[1] -= 2
        elif value == 1101:
            p[1] -= 1
        elif value == 11010:
            p[1] += 1
        elif value == 11110:
            p[1] += 2
        elif img[p[0]][p[1]-1] == 1 and img[p[0]][p[1]+1] == 1:
            p[1] -= 1
        if p[1] < l:
            l = p[1]
        elif p[1] > r:
            r = p[1]
    num1 = [[img[i][j] for j in range(r+1)] for i in range(h)]
    num2 = [[img[i][j] for j in range(l-1, w)] for i in range(h)]
    for i in range(h):
        for j in range(len(num1[0])-1, 0, -1):
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
    num1 = [[0 if num1[i][j] == 0 else 255 for j in range(len(num1[0]))] for i in range(len(num1))]
    num2 = [[0 if num2[i][j] == 0 else 255 for j in range(len(num2[0]))] for i in range(len(num2))]
    return [num1, num2]


if __name__ == '__main__':
    img = openImg()
    numList = dfa(img)
    cv2.imwrite(r"result/num1.jpg", numpy.array(numList[0], numpy.uint8))
    cv2.imwrite(r"result/num2.jpg", numpy.array(numList[1], numpy.uint8))
    print("DONE")