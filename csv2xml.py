import xml.etree.ElementTree as ET
import csv
import os


# 读取csv至字典
csvFile = open("t.csv", "r")
reader = csv.reader(csvFile)

# 建立空字典
transData = {}
title=None
for item in reader:
    if reader.line_num == 1:
        title=item
        continue
    transData[item[0]] = item
csvFile.close()

#所有输出文件
translateFiles=list()
for name in title:
    outDir=None
    if '中文' == name:
        outDir='./res/values-zh-rCN'
    if '英文' == name:
        outDir='./res/values-en'
    if not outDir:
        continue
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    xmlFile=os.path.join(outDir,'strings.xml')
    writer=open(xmlFile,'w')
    translateFiles.append(writer)

noTranslate=list()
with open('strings.xml','r') as templateF:
    for line in templateF:
        try:
            parsed=ET.fromstring(line)
            if parsed.text in transData:
                rowTrans=transData[parsed.text]
                for i,writer in enumerate(translateFiles):
                    if rowTrans[i]:
                        parsed.text=rowTrans[i]
                        writer.write(ET.tostring(parsed,encoding='unicode'))
                        writer.write('\n')
                    else:
                        parsed.text=rowTrans[0]
                        noTranslate.append(parsed.text)
                        writer.write(ET.tostring(parsed,encoding='unicode'))
                        writer.write('\n')
            else:
                noTranslate.append(parsed.text)
                for writer in translateFiles:
                    writer.write(ET.tostring(parsed,encoding='unicode'))
                    writer.write('\n')
        except:
            for writer in translateFiles:
                writer.write(line)

for writer in translateFiles:
    writer.close()

if noTranslate:
    print('下面的字符串没有翻译:')
    for s in noTranslate:
        print(s)