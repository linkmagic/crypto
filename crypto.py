import sys
import os.path


FILE_POS_DATA_LEN = 128
FILE_POS_DATA_START = 138


def loadText(textPath):
    with open(textPath, 'r') as textFile:
        data = textFile.read()
    return bytearray(data, 'utf-8')


def loadImage(imagePath):
    with open(imagePath, 'rb') as imageFile:
        data = imageFile.read()
    return bytearray(data)


def setDataLen(data, dataLen):
    resDataLen = bytearray(str(dataLen), 'utf-8')
    deltaZero = (FILE_POS_DATA_START - FILE_POS_DATA_LEN) - resDataLen.__len__()
    indexDataLen = FILE_POS_DATA_LEN

    while deltaZero:
        data[indexDataLen] = ord('0')
        indexDataLen = indexDataLen + 1
        deltaZero = deltaZero - 1

    indexResDataLen = 0
    while indexDataLen < FILE_POS_DATA_START:
        data[indexDataLen] = resDataLen[indexResDataLen]
        indexDataLen = indexDataLen + 1
        indexResDataLen = indexResDataLen + 1

    return data


def getDataLen(data):
    resDataLen = data[FILE_POS_DATA_LEN:FILE_POS_DATA_START]
    result = ''

    for ch in resDataLen:
        result = result + chr(ch)

    return int(result)


def encrypt(imagePath, textPath):
    dataTxt = loadText(textPath)
    dataTxtLen = dataTxt.__len__()
    dataImg = loadImage(imagePath)
    dataImgLen = dataImg.__len__()
    indexImg = FILE_POS_DATA_START
    indexTxt = 0

    setDataLen(dataImg, dataTxtLen)

    while indexImg < dataImgLen and indexTxt < dataTxtLen:
        dataImg[indexImg] = dataTxt[indexTxt]
        indexImg = indexImg + 3
        indexTxt = indexTxt + 1

    with open('imgresult.bmp', 'wb') as imgResult:
        imgResult.write(dataImg)


def decrypt(imagePath):
    dataImg = loadImage(imagePath)
    dataTxtLen = getDataLen(dataImg)
    resultTxt = []
    indexTxt = FILE_POS_DATA_START
    indexCh = 0

    while indexCh < dataTxtLen:
        resultTxt.append(dataImg[indexTxt])
        indexTxt = indexTxt + 3
        indexCh = indexCh + 1

    with open('txtresult.txt', 'w') as txtResult:
        txtResult.write(str(bytes(resultTxt)))


def fileExists(filePath):
    return os.path.exists(filePath)


argvHelp = """Cryptographer text in picture v1.0

USAGE:

encryption:\tcoder -e <image.bmp> <text.txt>
decryption:\tcoder -d <image.bmp>

help:\t\tcoder -h

Supported File formats:\t TXT, BMP
"""


def main():
    if sys.argv.__len__() < 3 or (sys.argv.__len__() == 2 and sys.argv[2] == '-h'):
        print(argvHelp)
    elif sys.argv.__len__() == 3 and sys.argv[1] == '-d':
        if fileExists(sys.argv[2]):
            decrypt(sys.argv[2])
            print('OK!')
        else:
            print('File ' + sys.argv[2] + ' does not exists')
    elif sys.argv.__len__() == 4 and sys.argv[1] == '-e':
        if fileExists(sys.argv[2]) and fileExists(sys.argv[3]):
            encrypt(sys.argv[2], sys.argv[3])
            print('OK!')
        else:
            print('One of the files ' + sys.argv[2] + ' or ' + sys.argv[3] + ' does not exists')
    else:
        print('Wrong format command\n', argvHelp)


if __name__ == '__main__':
    main()
