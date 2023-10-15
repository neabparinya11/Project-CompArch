file1 = open('result.txt', 'r')
file2 = open('fileCompare.txt', 'r')
file3 = open('resultCompare.txt', 'w')

file1_data = file1.readlines()
file2_data = file2.readlines()
for i in range(len(file1_data)):
    if file1_data[i] == file2_data[i]:
        print("line: ", i)
        file3.write("line: {} \n".format(i))
    else:
        print("line ", i, ":")
        # else print that line from both files
        print("\tFile 1:", file1_data[i], end='')
        print("\tFile 2:", file2_data[i], end='')
        file3.write("line: {}\n".format(i))
        file3.write("\tFile 1: {} \n".format(file1_data[i]))
        file3.write("\tFile 2: {} \n".format(file2_data[i]))

file1.close()
file2.close()
file3.close()