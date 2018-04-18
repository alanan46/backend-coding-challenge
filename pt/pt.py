
from pt_node import PTNode
"""
implementation of patricia tree
"""

class PT(object):
    def __init__(self):
        self.root = None

    # a wrapper
    def insert(self, key, datum):
        if(key is None or len(key) < 1):
            return
        if self.root is None:
            self.root = PTNode()
        self._insert(self.root, key, datum)

    def _insert(self, curNode, key, datum):
        ended = False
        for child in curNode.children:
            # find out the min length of 2 key
            keyLen = len(key) if len(key) < len(child.key) else len(child.key)
            i = 0
            while (i < keyLen):
                if (key[i] != child.key[i]):
                    break
                i += 1
            if i == 0:
                if key[i] < child.key[i]:
                    """
                        child = 'e' curNode ="ab" , use $ to mark isEnd
                            ab                        ab
                           /  \   insert c ->        / | \
                          e    G                    c$ e  G
                    """
                    node = PTNode(key, [datum])
                    node.isEnd = True
                    curNode.children.insert(curNode.children.index(child)+1,
                                            node)
                    ended = True
                    break
                else:
                    # case of key[0]> child.key[0]
                    continue
            else:
                # case of same prefix
                if i == keyLen:
                    if len(key) == len(child.key):
                        # case of duplicate geoname
                        if child.isEnd:
                            child.data.append(datum)  # append diff data
                        else:
                            """
                                    e.g. child="ab"
                                         ab                    ab$
                                        /  \    =========>    /   /
                                       e    f   insert "ab"  e     f

                            """
                            child.isEnd = True
                            child.data = [datum]
                    elif len(key) > len(child.key):
                              """
                                 e.g. child="ab$"
                                      ab$                    ab$
                                     /  /    ==========>    / | /
                                    e    f   insert "abc"  c$ e  f
                              """
                              self._insert(child, key[i:], datum)
                    else:
                        # copy child into a grandchild node
                        # with key as the diffed suffix
                        """
                          e.g. child="abc$"
                             abc$                      ab$
                            /   /      =========>      /
                           e     f     insert "ab"    c$
                                                     /  /
                                                    e    f
                        """

                        grandChildNode = PTNode(child.key[i:])
                        grandChildNode.isEnd = child.isEnd
                        grandChildNode.data = child.data
                        grandChildNode.children = child.children

                        child.key = key
                        child.isEnd = True
                        child.data = [datum]
                        child.children.append(grandChildNode)
                # 0< i <keyLen
                else:
                    """
                            e.g. child="abc$"
                         abc$                     ab
                        /  /     ==========>     / /
                       e    f   insert "abd"    c$  d$
                                               /  /
                                              e    f
                    """
                    # copy child into a grandChildNode with key modification
                    childSubkey = child.key[i:]
                    subkey = key[i:]
                    grandChildNode = PTNode(childSubkey)
                    grandChildNode.isEnd = child.isEnd
                    grandChildNode.data = child.data
                    grandChildNode.children = child.children

                    child.key = child.key[:i]
                    child.isEnd = False

                    node = PTNode(subkey)
                    node.isEnd = True
                    node.data = [datum]
                    child.children = []
                    if subkey[0] < childSubkey[0]:
                        child.children.append(node)
                        child.children.append(grandChildNode)
                    else:
                        child.children.append(grandChildNode)
                        child.children.append(node)
                ended = True
                break
        if not ended:
            node = PTNode(key)
            node.isEnd = True
            node.data = [datum]
            curNode.children.append(node)

    def find(self, key):
        if(key is None or len(key) < 1):
            return None
        if(self.root is None):
            return None
        return self._find(self.root, key)

    def _find(self, curNode, key):
        for child in curNode.children:
            keyLen = len(key) if len(key) < len(child.key) else len(child.key)
            i = 0
            while (i < keyLen):
                if (key[i] != child.key[i]):
                    break
                i += 1

            if i == 0:
                if key[0] < child.key[0]:
                    return None
                else:
                    continue
            else:
                if (i == keyLen):
                    if len(key) == len(child.key):
                        if child.isEnd:
                            return child.data
                        else:
                            return None
                    elif len(key) > len(child.key):
                        return self._find(child, key[i:])
                    else:
                        return None
                else:
                    return None
        return None
    # a wrapper
    def findSuffix(self, key):
            res = {}
            if(key is None or len(key) < 1):
                return res
            if(self.root is None):
                return res

            self._findSuffix(self.root, key, "", res)
            return res

    def _findSuffix(self, curNode, key, prefix, res):
        for child in curNode.children:
            keyLen = len(key) if len(key) < len(child.key) else len(child.key)
            i = 0
            while (i < keyLen):
                if (key[i] != child.key[i]):
                    break
                i += 1

            if i == 0:
                continue
            else:
                if (i == keyLen):
                    if key in child.key:
                        self.findall(child, prefix+child.key, res)
                    elif len(key) > len(child.key):
                        self._findSuffix(child, key[i:], prefix+child.key, res)

    # given a node find all the children nodes data
    def findall(self, curNode, prefix, res):
        if curNode is None:
            return
        if curNode.isEnd:
            res[prefix] = curNode.data
        for child in curNode.children:
            self.findall(child, prefix+child.key, res)
