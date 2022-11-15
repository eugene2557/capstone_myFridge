from datetime import datetime

class Scene:
    def __init__(self, cnt, items:list):
        self.cnt = cnt
        self.time = datetime.now()
        self.items = items
    
    def __str__(self):
        return '* Scene\ncnt: {0} \nitems: {1} \n*'.format(self.cnt, self.items)


class Item:
    def __init__(self, cnt, cls, x, y, w, h):
        self.cnt = cnt
        self.cls = cls
        self.time = datetime.now()

        # points
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # if exists last time
        self.status = 'in'
        self.before = None
        self.after = None

    def __str__(self):
        return '* Item\ncnt: {0} cls: {1} status: {2} x: {3}\n*'.format(self.cnt, self.cls, self.status, self.x)

class Dnode:
    def __init__(self, scene:Scene, prev=None, next=None):
        self.scene = scene
        self.prev = prev
        self.next = next

    def __str__(self):
        return '* Dnode \nscene: {0} \n*'.format(self.scene)


class DList:
    def __init__(self):
        self.head = None
        self.ptr = None # points last obj
        self.cnt = 0
   
    def insert(self, scn):
        dnode = Dnode(scn, self.ptr, None)
        if self.head == None:
            self.head = dnode
        if self.ptr != None:
            self.ptr.next = dnode
        self.ptr = dnode
        self.cnt += 1
    
    def search(self, idx):
        p = self.head
        while p != None:
            if p.scene.cnt == idx:
                return p
            p = p.next

    def print(self):
        p = self.ptr
        print('** DList')
        while p != None:
            print(p.scene)
            p = p.prev
        print('**')