from django.shortcuts import render

PATH2 = "./static/points_re.txt"

# Create your views here.
def fridge(request):
    ci_lst = []
    iot_lst = []
    epff_lst = []
    ic_lst = []
    re = open(PATH2, 'r', encoding='UTF8')
    lines = re.readlines()

    print(lines)

    for i in range(len(lines)):
        line = lines[i]

        if i % 6 == 0:
            line = list(map(int, line.split()))
            ci_lst.append(line)
        elif i % 6 == 2:
            if line == "\n":
                continue
            iot_lst.append(line)
        elif i % 6 == 3 or i % 6 == 4:
            if line == "\n":
                continue
            epff_lst.append(line)
        elif i % 6 == 5:
            line = list(map(int, line.split()))
            ic_lst.append(line)


    re.close()
    return render(request, 'fridge.html', {'ci' : ci_lst[-1], 'iot' : iot_lst, 'epff' : epff_lst, 'ic' : ic_lst[-1]})


