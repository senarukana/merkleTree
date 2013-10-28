from math import log,pow,ceil
import md5 

class MerkleTree(object):
    def __init__(self, object_list):
        # calculate the real height:
        # formula is height =  ceil(log(len,2)) + 1
        self.treeHeight = int(ceil(log(len(object_list),2)) + 1)
        print self.treeHeight
        # init tree data
        self.trees = ['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'] * int((pow(2, self.treeHeight - 1)) + len(object_list))
        self.object_list = object_list
        self.fill_trees()
    

    def fill_trees(self):
        # we first calulate the data md5 at the leaf node 
        startoffset = int(pow(2, self.treeHeight - 1))
        for i in range(0, len(self.object_list), 2):
            # at each loop we calculate the left, right and parent node together
            # left node
            m1 = md5.new()
            m1.update(str(self.object_list[i]))
            self.trees[startoffset + i] = m1.digest()
            if i + 1 < len(self.object_list):
                # right node
                m2 = md5.new()
                m2.update(str(self.object_list[i + 1]))
                self.trees[startoffset + i + 1] = m2.digest()
                # we also need to merge left and right to parent md5 value
                m1.update(str(self.object_list[i + 1]))
            # parent node
            self.trees[int((startoffset + i) / 2)] = m1.digest()
       
        # calculate the data from buttom, we need to merge child node md5 to parent md5 value 
        for i in range(1, self.treeHeight - 1):
            curHeight = self.treeHeight - i - 1
            start = int(pow(2,curHeight - 1))
            end = int(pow(2, curHeight) - 1)
            for index in range(start, end+1):
                m = md5.new()
                m.update(self.trees[index * 2])
                m.update(self.trees[index * 2 + 1])
                self.trees[index] = m.digest()
        print self.trees

    def trees(self):
        return self.trees

# store diff between tree1 and tree2
diff = []
def _recursive(tree1, tree2, index, height):
    if height == tree.treeHeight:
        print  "%d, %d" % (index, height )
        if index +1 > len(tree2.trees) or tree1.trees[index] != tree2.trees[index]:
            pos = index - (len(tree1.trees) - len(tree1.object_list))
            diff.append("position:%d, value:%d is different" % \
                (pos, tree1.object_list[pos]))
    else:
        if tree1.trees[index] != tree2.trees[index]:
            _recursive(tree1,tree2, index * 2, height + 1)
            if index * 2 + 1 < len(tree1.trees):
                _recursive(tree1,tree2, index * 2 + 1, height + 1)


def cmp(tree1, tree2):
    if len(tree2.trees) > len(tree1.trees):
        _recursive(tree2, tree1, 1, 1)
    else:
        _recursive(tree1, tree2, 1, 1)

    print diff


a = [6,2,9,7,3,6,5]
tree = MerkleTree(a)
b = [6,2,9,7,6,10,1]
tree1 = MerkleTree(b)
cmp(tree,tree1)



