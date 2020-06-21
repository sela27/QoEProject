import divider
from datetime import datetime

if __name__ == '__main__':

    # divider.Divider.make_csv()

    times = divider.Divider.cut_ocr_csv()  # get times + ocr csv cuts

    divider.Divider.cut_pcap_csv(times)  # get pcap csv cuts using the times












    # times = ['11:48:01.123415', '11:49:02.326214', '11:49:02.672532', '11:50:00.152326']
    # times = ['17:25:54', '17:29:19', '17:29:20', '17:29:26', '17:29:27', '17:32:56', '17:32:57', '17:33:57',
    #          '17:33:57', '17:34:55', '17:34:56', '17:35:08', '17:35:08', '17:41:12', '17:41:13', '17:41:23',
    #          '17:41:24', '17:41:33', '17:41:33', '17:42:44']
    # for i in range(len(times)):
    #     print(times[i])

    # divider.Divider.cut_pcap_csv(times)  # get pcap csv cuts using the times

    # checking the remove end function
    # str = "o9aaoilecM [dash-otf]"
    # str = "09tX391Cn?U‘lvodl'"
    # str = "09a aoivJ lc'M'IIda‘stkot?"
    # str = divider.Divider.remove_end(str) # if the delimiter is not present, it returns an empty string!!!!
    # print(str)


    # pcaptime = "May 15, 2020 11:48:02.264677000 Jerusalem Daylight Time"

    # pcaptime = pcaptime.split(":")
    # time = pcaptime[0][len(pcaptime[0])-2:len(pcaptime[0])]+":"+pcaptime[1]+":"+pcaptime[2][0:2]
    # print(time)

    # time_str = 'bla bla 13:55:26.12153151 bla bla'
    # temp_time_holder = time_str.split(":")
    # time_str = temp_time_holder[0][len(temp_time_holder[0])-2:len(temp_time_holder[0])] + ":" + temp_time_holder[1] + ":" + temp_time_holder[2][0:9]
    # time_str2 = '13:55:27.231222'
    #
    # time_object1 = datetime.strptime(time_str, '%H:%M:%S.%f').time()
    # time_object2 = datetime.strptime(time_str2, '%H:%M:%S.%f').time()
    #
    # if time_object1 > time_object2:
    #     print("at if")
    #     print(time_object1)
    # else:
    #     print("at else")
    #     print(time_object2)

    # print(type(time_object))
    # print(time_object)


    # check = datetime.datetime("11:48:02")
    # print(check)








    # check1 = "a"+""+"b"
    # check2 = "a"+" "+"b"
    # print(check1)
    # print(check2)

    # str = 'a?aaaivJ ch [dash-otf]'
    # str = str.replace(" ","")
    # print(str)

     # Dynamic Programming implementation of LCS problem




     # # Driver program to test the lcs func
     # x = "AGGTAB"
     # y = "GXTXAYB"
    # x = "09a aoivJ"
    # y = "o9aaoilecM"
    # x = "o9aaoilecM"
    # y = "T99e041quE"
    # x = "o9aaoilecM [dash—otf]"
    # y = "T99e041quE [dash-otf]" ???
    # x = "o9aaoilecM [dash—otf]" ???
    # y = "T99e041quE [dash-otf]"
    # x = "ad"
    # y = "sd"

    # x = divider.Divider.remove_end(x)
    # y = divider.Divider.remove_end(y)
    # print(x)
    # print(y)
    # ans = divider.Divider.lcs(x, y, len(x), len(y))
    # print("Length of LCS is: " + str(ans))

    # str1 = "abcd"

    # ans = str1[0:(len(str1))]
    # print(ans)