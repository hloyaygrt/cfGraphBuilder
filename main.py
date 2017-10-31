import urllib2
import json
import time


def printToFile(l, handle):
    a = list(l.items())
    a.sort()

    pureData = open(handle + '_data.txt', 'w')
    f = open('got_data.txt', 'w')

    for e in a:
        f.write('["' + str(e[0][0]) + '/' + str(e[0][1]) + '/' + str(e[0][2]) + '", ' + str(e[1]) + ']' + ', ')
        pureData.write(str(e[0][0]) + ' ' + str(e[0][1]) + ' ' + str(e[0][2]) + '=' + str(e[1]) + '\n')


def printToScriptFile(l, handle):
    a = list(l.items())
    a.sort()

    res = ''
    i = 0

    for e in a:
        res += '["' + str(e[0][0]) + '/' + str(e[0][1]) + '/' + str(e[0][2]) + '", ' + str(e[1]) + ']'
        if i != len(a) - 1:
            res += ', '
        i += 1
    f = open('Result.html', 'r')

    resWeHave = f.read()
    norm_shablon = 'var data = [\n\t\t{\n\t\t\tlabel: "' + str(handle) + '",\n\t\t\tdata: [' + res + ']\n\t\t},'

    newRes = resWeHave.replace('var data = [', norm_shablon)

    f = open('Result.html', 'w')
    f.write(newRes)


def deleteFromScriptFile(handle):
    f = open('Result.html', 'r')
    s = f.read()

    pos = s.find(handle)
    if pos == -1:
        return
    while s[pos] != '{':
        pos -= 1
    pos2 = pos
    while s[pos2] != '}':
        pos2 += 1

    newRes = ''
    i = 0
    while i < pos:
        newRes += s[i]
        i += 1
    i = pos2 + 2
    while i < len(s):
        newRes += s[i]
        i += 1
    f = open('Result.html', 'w')
    f.write(newRes)


h1 = raw_input('Write handle.\n')

while True:
    type = raw_input('Do you want to add or del him? ("add" / "del")\n')
    if type == 'add' or type == '"add"':
        break
    if type == 'del' or type == '"del"':
        deleteFromScriptFile(h1)
        exit(0)

mappyMap = dict()

cnt_looked = 0
ans = 0
cnt = 1

while True:
    #print(cnt_looked // 500)
    print('Loading' + cnt * '.')
    cnt += 1
    if cnt == 4:
        cnt = 1

    query = json.load(urllib2.urlopen('http://codeforces.com/api/user.status?handle=' + h1 + '&from=' +
                                      str(cnt_looked + 1) + '&count=500'))

    while query['status'] == 'FAILED':
        query = json.load(urllib2.urlopen('http://codeforces.com/api/user.status?handle=' + h1 + '&from=' +
                                          str(cnt_looked + 1) + '&count=500'))
    submissionList = query['result']
    if len(submissionList) == 0:
        break
    for submission in submissionList:
        if submission['verdict'] == 'OK':
            #problem = submission['problem']

            unixTime = submission['creationTimeSeconds']

            year = int(time.strftime("%Y", time.localtime(unixTime)))
            month = int(time.strftime("%m", time.localtime(unixTime)))
            day = int(time.strftime("%d", time.localtime(unixTime)))

            day = 1
            ans += 1

            #print(str(year) + '/' + str(month) + '/' + str(day))
            try:
                mappyMap[(year, month, day)] += 1
            except:
                mappyMap[(year, month, day)] = 1
    cnt_looked += 500

print('Totally times accepted:', ans)
#printToFile(mappyMap, h1)
printToScriptFile(mappyMap, h1)