from classes import DList, Scene, Item
from datetime import timedelta, datetime
import time

classes = ['사과', '양상추', '귤', '양파', '파프리카', '배', '호박', '포도', '아보카도', '감자']
expired_date = [1, 1, 3, 3, 5, 5, 300, 8, 10, 10]
in_cnt = [0 for i in range(len(classes))]

dlist = DList()

def cls_classifier(data):
    for i in range(len(data)):
        data[i] = round(float(data[i]), 6)
        if i % 6 == 0 or i % 6 == 1:
            data[i] = int(data[i])

    if len(data) == 2:
        item = Item(0, -1, -1, -1, -1, -1)
        item.status = 'empty'
        # print(item)
        scene = Scene(data[0], [item])
        # print(scene)
        dlist.insert(scene)
        # print(dlist.head)
        # print(dlist.ptr.prev)
        # print(dlist.ptr.next)
    else:
        num = len(data) // 6
        items = []
        for i in range(num):
            item = Item(i+1, data[i*6+1], data[i*6+2], data[i*6+3], data[i*6+4], data[i*6+5])
            # print(item)
            items.append(item)
        scene = Scene(data[0], items)
        # print(scene)
        dlist.insert(scene)
        # print(dlist.head)
        # print(dlist.ptr.prev)
        # print(dlist.ptr.next)
    
           
def current_items(idx):
    scn = dlist.search(idx)

    cnt = scn.scene.cnt
    time = scn.scene.time

    n_items = [0 for i in range(10)]

    if scn.scene.items[0].cls == -1:
        # print(cnt, time, n_items)
        return n_items, cnt, time
    
    for i in range(len(scn.scene.items)):
        for j in range(10):
            if scn.scene.items[i].cls == j:
                n_items[j] += 1
    
    # print(cnt, time, n_items)
    return n_items, cnt, time


def compare_items(idx):
    if idx == 0:
        scn = dlist.search(idx).scene
        for item in scn.items:
            if item.status == 'in':
                in_cnt[item.cls] += 1
        return

    scn = dlist.search(idx)
    scn_p = dlist.search(idx-1)

    if scn.scene.items[0].status == 'empty':
        for item_p in scn_p.scene.items:
            item_p.status = 'out'
        return
    

    n_items, cnt, time = current_items(idx)
    p_n_items, p_cnt, p_time = current_items(idx-1)

    # compare and find if exists or out
    for i in range(10):
        if n_items[i] != 0 and p_n_items[i] != 0:
            for item in scn.scene.items:
                for item_p in scn_p.scene.items:
                    if item.cls == item_p.cls:
                        if (item_p.x-0.02 <= item.x <= item_p.x+0.02) and (item_p.y-0.02 <= item.y <= item_p.y+0.02):  
                            item.status = 'exisiting'
                            item.before = item_p
                            item_p.after = item
        elif p_n_items[i] != 0 and n_items[i] == 0:
            for item_p in scn_p.scene.items:
                if item_p.cls == i:
                    item_p.status = 'out'
                    item_p.after = None  
                   

    for i in range(10):
        if n_items[i] != 0 and p_n_items[i] != 0:
            for item_p in scn_p.scene.items:
                flg = False
                for item in scn.scene.items:
                    if item_p.cls == item.cls and (item_p.x-0.02 <= item.x <= item_p.x+0.02) and (item_p.y-0.02 <= item.y <= item_p.y+0.02):  
                        flg = True
                if flg == False:
                    item_p.status = 'out'
                    item_p.after = None

    for item in scn.scene.items:
        if item.status == 'in':
            in_cnt[item.cls] += 1
    



    # for item_p in scn_p.scene.items:
    #     for item in scn.scene.items:
    #         if item_p.cls == item.cls:
    #             if (item_p.x-0.02 <= item.x <= item_p.x+0.02) and (item_p.y-0.02 <= item.y <= item_p.y+0.02):
    #                 break
    #             elif item.cnt != len(scn.scene.items):  # 다음 cls 같은 item이 있는 경우 out 처리하면 안됨
    #                 break   # 이렇게 처리하면 다음 cls 다른 item이 있는 경우(더이상 cls 비교 대상 없는 경우) out 처리 안됨
    #             item_p.status = 'out'
    #             item_p.after = None
    

def in_and_out(idx):    
    scn = dlist.search(idx)

    in_lst = []
    out_lst = []

    # in list
    for item in scn.scene.items:
        if item.status == 'in':
            in_lst.append(item)
        elif item.status == 'empty':
            in_lst = []
    
    # out list
    if idx != 0:
        scn_p = dlist.search(idx-1)
        for p_item in scn_p.scene.items:
            if p_item.status == 'out':
                out_lst.append(p_item)

    # empty
    if out_lst:
        if out_lst[0].cls == -1:
            out_lst = []
    
    return in_lst, out_lst


def expired_check(idx):
    scn = dlist.search(idx).scene
    first_in = []
    expired = []

    if idx == 0:
        return first_in

    # empty
    if scn.items[0].cls == -1:
        return first_in
    
    # first-in
    for item in scn.items:
        t = item
        while t.before != None:
            # print(t)
            t = t.before
        first_in.append(t)

    # check expired
    for t in first_in:
        for i in range(10):
            if t.cls == i:
                if t.time + timedelta(seconds=expired_date[i]) < datetime.now():
                    # print(datetime.now())
                    # print(t.time)
                    expired.append(t)
    return expired


def fifo(idx):
    fifo_lst = []

    if idx == 0:
        return fifo_lst
    
    scn = dlist.search(idx).scene
    scn_p = dlist.search(idx-1).scene

    if scn.items[0].cls == -1:
        # print(fifo_lst)
        return fifo_lst

    for p_item in scn_p.items:
        if p_item.status == 'out':
            for t in scn_p.items:
                if p_item.cls == t.cls:  
                    while t.before != None:
                        t = t.before
                    if t.time < p_item.time:
                        if t.x != p_item.x and t.cls != 4 and t.cls != 6:
                            fifo_lst.append(t)
    return fifo_lst





def log(data, idx):
    cls_classifier(data)
    compare_items(idx)

    n_items, cnt, time = current_items(idx)
    in_lst, out_lst = in_and_out(idx)
    expired = expired_check(idx)
    fifo_lst = fifo(idx)


    # time = time.strftime('%y.%m.%d %H:%M:%S')
    time = time.strftime('%H:%M:%S')



    # api: current_items
    if n_items.count(0) == 10:
        rs_current_items = ""
    else:
        rs_current_items = "[" + time + "] "
        for i in range(len(n_items)):
            if n_items[i] == 0:
                continue
            rs_current_items += f'[{classes[i]}] {n_items[i]}개'
            if n_items[i+1:].count(0) != len(n_items)-i-1:
                rs_current_items += ', '
        rs_current_items += "이(가) 있습니다."
    
    # api: in_and_out
    # in
    rs_in = ""
    in_cls = []
    for item in in_lst:
        in_cls.append(item.cls)
    
    for i in range(len(classes)):
        if in_cls.count(i) == 0:
            continue
        rs_in += f'[{classes[i]}] {in_cls.count(i)}개, '
    
    if rs_in:
        rs_in = rs_in[:len(rs_in)-2]

    # out
    rs_out = ""
    out_cls = []
    for item in out_lst:
        out_cls.append(item.cls)
    
    for i in range(len(classes)):
        if out_cls.count(i) == 0:
            continue
        rs_out += f'[{classes[i]}] {out_cls.count(i)}개, '
    
    if rs_out:
        rs_out = rs_out[:len(rs_out)-2]

    # in_and_out
    if rs_in and rs_out:
        rs_in += '가(이) 들어오고 '
        rs_out += '가(이) 나갔습니다.'
        rs_in_and_out = "[" + time + "] " + rs_in + rs_out
    elif rs_in and not rs_out:
        rs_in += '가(이) 들어왔습니다.'
        rs_in_and_out = "[" + time + "] " + rs_in
    elif not rs_in and rs_out:
        rs_out += '가(이) 나갔습니다.'
        rs_in_and_out = "[" + time + "] " + rs_out
    else:
        rs_in_and_out = ""

    # api = expired
    exp_cls = []
    # rs_exp = "[" + time + "] [유통기한] "
    rs_exp = "[유통기한] "

    if not expired:
        rs_exp = ""
    # for item in expired:
    #     exp_cls.append(item.cls)
    
    # for i in range(len(classes)):
    #     if exp_cls.count(i) == 0:
    #         continue
    #     rs_exp += f'[{classes[i]}] {exp_cls.count(i)}개(), '

    for exp in expired:
        dif = str(datetime.now() - exp.time)[:7]
        rs_exp += f'{classes[exp.cls]}({dif}), '
    
    if rs_exp:
        rs_exp = rs_exp[:len(rs_exp)-2] + ' 초과'
    
    # api: fifo
    fifo_lst_2 = []
    # rs_fifo = "[" + time + "] [선입선출] "
    rs_fifo = "[선입선출] "

    if not fifo_lst:
        rs_fifo = ""

    for item in fifo_lst:
        if item.cls not in fifo_lst_2:
            fifo_lst_2.append(item)
    
    for item in fifo_lst_2:
        for i in range(len(classes)):
            if item.cls == i:
                rs_fifo += f'{classes[i]}({item.time.strftime("%H:%M:%S")}), '
    
    if rs_fifo:
        rs_fifo = rs_fifo[:len(rs_fifo)-2] + ' 위반'

    print(n_items)
    print(rs_current_items)
    print(rs_in_and_out)
    print(rs_exp)
    print(rs_fifo)
    print(in_cnt)

    return n_items, rs_current_items, rs_in_and_out, rs_exp, rs_fifo, in_cnt
    
        
    # in and out
    # print("* in_lst : ")
    # for item in in_lst:
    #     print(item.cls)
    # print("*")
    # print("* out_lst : ")
    # for item in out_lst:
    #     print(item.cls)
    # print("*")
    
    # expired
    # print("* expired : ")
    # for item in expired:
    #     print(item.cls, item.time)
    # print("*")

    # fifo
    # print("* fifo : ")
    # for item in fifo_lst:
    #     print(item.cls, item.time)
    # print("*")



if __name__ == "__main__":
    
    a = "0 4 0.264844 0.934375 0.176563 0.13125"
    b = "1 4 0.264844 0.934375 0.176563 0.13125\n1 4 0.932031 0.146875 0.132812 0.285417\n1 5 0.477344 0.513542 0.954687 0.90625"
    c = "2 4 0.264844 0.934375 0.176563 0.13125\n2 5 0.477344 0.513542 0.954687 0.90625\n2 6 0.835156 0.508333 0.329688 0.916667\n2 9 0.364844 0.589583 0.185937 0.2375"
    d = "3 4 0.264844 0.934375 0.176563 0.13125\n3 5 0.477344 0.513542 0.954687 0.90625\n3 2 0.535156 0.65 0.473437 0.5125\n3 3 0.617969 0.507292 0.710938 0.977083"
    e = "4 5 0.477344 0.513542 0.954687 0.90625\n4 2 0.535156 0.65 0.473437 0.5125\n4 3 0.364844 0.589583 0.185937 0.2375\n4 5 0.835156 0.508333 0.329688 0.916667\n4 4 0.827344 0.84375 0.335938 0.308333"
    f = "5 -1"
    g = "6 -1"
    h = "7 1 0.261719 0.930208 0.173438 0.139583\n7 1 0.617969 0.507292 0.710938 0.977083"

    a = a.split()
    b = b.split()
    c = c.split()
    d = d.split()
    e = e.split()
    f = f.split()
    g = g.split()
    h = h.split()

    print(0)
    log(a, 0)
    time.sleep(3)

    print(1)
    log(b, 1)
    time.sleep(4)

    print(2)
    log(c, 2)
    time.sleep(2)

    print(3)
    log(d, 3)
    time.sleep(5)

    print(4)
    log(e, 4)
    time.sleep(3)

    print(5)
    log(f, 5)
    time.sleep(4)

    print(6)
    log(g, 6)
    time.sleep(1)

    # print(7)
    # log(h, 7)
    # time.sleep(1)

    

    print(0)
    for item in dlist.search(0).scene.items:
        print(item)
    print()

    print(1)
    for item in dlist.search(1).scene.items:
        print(item)
    print()

    print(2)
    for item in dlist.search(2).scene.items:
        print(item)
    print()

    print(3)
    for item in dlist.search(3).scene.items:
        print(item)
    print()

    print(4)
    for item in dlist.search(4).scene.items:
        print(item)
    print()

    print(5)
    for item in dlist.search(5).scene.items:
        print(item)
    print()

    print(6)
    for item in dlist.search(6).scene.items:
        print(item)
    print()




    # for i in range(7):
    #     for item in dlist.search(i).scene.items:
    #         print(item)
