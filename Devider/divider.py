import os
import csv
from datetime import datetime

# tshark_pcap_to_csv = 'C:\\"Program Files"\\Wireshark\\tshark.exe -r [src] -T fields -e frame.number -e frame.time -e frame.len -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e tcp.window_size -e tcp.options.wscale.shift -e tcp.analysis.keep_alive -e tcp.options.mss_val -e tcp.flags.ack -e tcp.flags.syn -e tcp.ack -e tcp.flags.reset -e frame.time_epoch -e gquic.tag.sni -E header=y -E separator=, -E quote=d -E occurrence=f > [dst]'
tshark_pcap_to_csv = 'C:\\"Program Files"\\Wireshark\\tshark.exe -r [src] -T fields -e frame.number -e frame.time -e frame.len -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e ssl.handshake.session_id_length -e ssl.handshake.comp_methods_length -e ssl.handshake.extension.len -e ssl.handshake.cipher_suites_length -e tcp.window_size -e tcp.options.wscale.shift -e tcp.analysis.keep_alive -e tcp.options.mss_val -e ssl.handshake.version -e frame.time_delta -e ip.ttl -e ssl.handshake.extensions_server_name -e tcp.flags.ack -e tcp.flags.syn -e tcp.ack -e tcp.flags.reset -e frame.time_epoch -e gquic.tag.sni -E header=y -E separator=, -E quote=d -E occurrence=f > [dst]'


class Divider:

    @staticmethod
    def make_csv():
        for dirName, subdirList, fileList in os.walk('C:\\Users\\zzkmp\\Desktop\\Present'):
            for fname in fileList:
                if fname.endswith('.pcap') and fname.replace('.pcap', '.csv') not in fileList:
                    os.system(tshark_pcap_to_csv.replace('[src]', os.path.join(dirName, fname))
                              .replace('[dst]', os.path.join(dirName, fname.replace('.pcap', '.csv'))))

    # cuts the vid-csv into n sub vid-csv's and returns an array that
    # holdes the start and stop times of all videos in order.
    # Example: even index (includes 0) is start time, odd index is end time of each vid
    # so first vid start time is at time[0] and end at time[1] and so on...
    @staticmethod
    def cut_ocr_csv():
        input_path = 'C:\\Users\\zzkmp\\Desktop\\Present\\ocr.csv'
        # path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\NewTests\\scrCopy\\vid\\test.csv'
        # path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\oldVersionTests\\test2\\results.csv'
        with open(input_path, 'r') as f:
            temp_ocr = []
            vid_start_stop_time = []  # even index with 0 is start time, odd index is end time of each vid
            reader = csv.reader(f)
            field_names = next(reader)   # get the field names from the ocr file
            first_line = next(reader)    # get the first line for comparison with second
            temp_ocr.append(first_line)  # manually append the first line for the first csv
            prev = first_line[3]         # get the prev of the first (id name)
            temp_time = first_line[0]
            vid_start_stop_time.append(temp_time)  # insert first start time
            csv_num = 1
            count_misread_rows = 0
            for row in reader:

                # the previous "if", changed it by removing those same endings
                # the -6 len is to avoid evaluating the similar endings like [vod] and more..
                # if Divider.lcs(prev[0:(len(prev))-6], row[3][0:(len(row[3]))-6], len(prev)-6, len(row[3])-6) >= 6:

                id_prev = Divider.remove_end(prev)
                id_current = Divider.remove_end(row[3])
                if Divider.lcs(id_prev, id_current, len(id_prev), len(id_current)) >= 5:
                    temp_ocr.append(row)
                    prev = row[3]
                    temp_time = row[0]  # get next time

                # the previous "if" is instead of this one
                # if Devider.check_same_id(id_prev, id_current):
                #     temp_ocr.append(row)
                #     prev = row[3]

                # second chance to find misread "same id" lines by the OCR
                # logic: if your not different then your same
                elif not(Divider.check_diff_id(id_prev, id_current)):
                    count_misread_rows += 1
                    temp_ocr.append(row)
                    prev = row[3]
                    temp_time = row[0]  # get next time
                    print("OCR ID Evaluation ERROR at line: " + str(row))

                # else were creating the csv file with the collected data
                else:  # this is the logic ==> Devider.check_diff_id(prev, row[3]):
                    vid_start_stop_time.append(temp_time)  # end time of the current video
                    temp_time = row[0]  # start time of the next video
                    vid_start_stop_time.append(temp_time)

                    file_name = "ocr" + ".csv"
                    dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)
                    output_path = os.path.join(dir_path, file_name)

                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    else:
                        while os.path.exists(dir_path):
                            csv_num += 1
                            dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)

                        output_path = os.path.join(dir_path, file_name)
                        os.makedirs(dir_path)

                    with open(output_path, mode='w') as csv_file:
                        writer = csv.writer(csv_file, lineterminator='\n')
                        writer.writerow(field_names)
                        for i in range(len(temp_ocr)):
                            writer.writerow(temp_ocr[i])

                    temp_ocr.clear()
                    temp_ocr.append(row)  # the first row of different ID name
                    prev = row[3]
                    csv_num += 1

            # last csv (or first if only one) creation is manual
            vid_start_stop_time.append(temp_time)  # end time of the current
            file_name = "ocr" + ".csv"
            dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)
            output_path = os.path.join(dir_path, file_name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            else:
                while os.path.exists(dir_path):
                    csv_num += 1
                    dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)

                file_name = "ocr" + ".csv"
                output_path = os.path.join(dir_path, file_name)
                os.makedirs(dir_path)

            with open(output_path, mode='w') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                writer.writerow(field_names)
                for i in range(len(temp_ocr)):
                    writer.writerow(temp_ocr[i])

        if count_misread_rows != 0:
            print("Total misread rows: " + str(count_misread_rows))

        return vid_start_stop_time


    @staticmethod
    def cut_pcap_csv(times):  # TODO continue to change code here too and check that it always works(if else everything)

        path = 'C:\\Users\\zzkmp\\Desktop\\Present\\pcap.csv'

        with open(path, 'r') as f:
            temp_pcap = []
            reader = csv.reader(f)
            field_names = next(reader)   # get the field names from the pcap file
            csv_num = 1
            index = 0  # the index for the ocr start and end times
            # print("index is: " + str(index))
            ocr_start_time_object = datetime.strptime(times[index], '%H:%M:%S').time()

            index += 1
            ocr_end_time_object = datetime.strptime(times[index], '%H:%M:%S').time()
            # print("index is: " + str(index))
            for row in reader:

                temp_time_holder = row[1].split(":")  # an array of 3 that holds: str:str:str (of the pcap)
                # extracting the time (creating time str)
                # print(temp_time_holder[2][0:9])
                pcap_time = temp_time_holder[0][len(temp_time_holder[0])-2:len(temp_time_holder[0])]+":"+temp_time_holder[1]+":"+temp_time_holder[2][0:2]
                # creating time object
                pcap_time_object = datetime.strptime(pcap_time, '%H:%M:%S').time()

                # if the pcap started before the ocr then wait until the pcap csv catches up to the ocr start time
                if ocr_start_time_object > pcap_time_object:
                    continue

                # collect the packets of the current vid (by times)
                elif (ocr_start_time_object <= pcap_time_object) and (pcap_time_object < ocr_end_time_object):
                    temp_pcap.append(row)

                elif times[len(times)-1] == str(ocr_end_time_object):  # if were done, stop. (times[len(times)-1] is the final time)
                    break

                else:  # pcap_time_object >= ocr_end_time_object:
                    file_name = "pcap" + ".csv"
                    dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)
                    output_path = os.path.join(dir_path, file_name)

                    check_file_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num) + "\\" + file_name

                    if not os.path.exists(dir_path):
                        print("The folder at path: " + dir_path + " Does now exist, Stopping!")
                        return

                    elif os.path.exists(check_file_path):
                        while os.path.exists(check_file_path):
                            csv_num += 1
                            check_file_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num) + "\\" + file_name
                            dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)
                        output_path = os.path.join(dir_path, file_name)

                    with open(output_path, mode='w') as csv_file:
                        writer = csv.writer(csv_file, lineterminator='\n')
                        writer.writerow(field_names)
                        for i in range(len(temp_pcap)):
                            writer.writerow(temp_pcap[i])

                    index += 1
                    ocr_start_time_object = datetime.strptime(times[index], '%H:%M:%S').time()
                    index += 1
                    ocr_end_time_object = datetime.strptime(times[index], '%H:%M:%S').time()

                    temp_pcap.clear()
                    csv_num += 1

            # last csv (or first if only one) creation is manual
            file_name = "pcap" + ".csv"
            dir_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid" + str(csv_num)
            output_path = os.path.join(dir_path, file_name)

            if not os.path.exists(dir_path):
                print("The folder at path: " + dir_path + "Does now exist, Stopping!")
                return

            with open(output_path, mode='w') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                writer.writerow(field_names)
                for i in range(len(temp_pcap)):
                    writer.writerow(temp_pcap[i])

    @staticmethod
    def remove_end(id_name):  # by finding the last whitespace
        index = 0
        run = 0
        for i in id_name:
            if i == " ":
                index = run
            run += 1

        if index != 0:
            return id_name[0:index]

        else:
            return id_name[0:len(id_name)]  #  in case the ocr misread space for somt else, just work with
                                            #  the original word

    # an O(n^2) lcs, there are better implementations but for now this one is sufficient.
    @staticmethod
    def lcs(prev, new, m, n):
        if m == 0 or n == 0:
            return 0
        elif prev[m - 1] == new[n - 1]:
            return 1 + Divider.lcs(prev, new, m - 1, n - 1)
        else:
            return max(Divider.lcs(prev, new, m, n - 1), Divider.lcs(prev, new, m - 1, n))

    #  older version method, not used for now (lcs is better)
    @staticmethod
    def check_same_id(prev, new):  # goes by probability (99% of the times it will be good enough, could be fixed a bit)

        if len(prev) >= len(new):
            smaller_word = new
        else:
            smaller_word = prev
        same = 0
        i = 0
        j = 0
        while i < len(smaller_word)-5 and j < len(smaller_word)-5:
            if prev[i] == " ":
                i += 1
            if new[j] == " ":
                j += 1
            if prev[i] == new[j]:
                same = same + 1
            i += 1
            j += 1
        if same >= 4:  # by experience at least 4 is needed, but could be more!
            return True
        else:
            return False

    @staticmethod
    def check_diff_id(prev, new):

        if len(prev) >= len(new):
            smaller_word = new
        else:
            smaller_word = prev

        # print(smaller_word)
        diff = 0
        i = 0
        j = 0

        while i < len(smaller_word)-1 and j < len(smaller_word)-1:
            try:
                if prev[i] == " ":
                    i += 1

                if new[j] == " ":
                    j += 1

                if prev[i] != new[j]:
                    diff = diff + 1

                i += 1
                j += 1

            except:
                print(prev)
                print(new)
                print("Prev is: " + str(len(prev)))
                print("new is: " + str(len(new)))
                print("while until count : " + str(len(smaller_word)))
            #     print(i)
            #     print("An exception occurred")
                return

        if diff > len(smaller_word)/2:  # trying to be strict
            return True
        else:
            return False


