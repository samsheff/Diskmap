import os
from node import Node
from file import File
from directory import Directory


class Treemap(object):
    '''A Treemap class.'''

    def __init__(self):
        '''Create a new Treemap.'''
        self.root = None

    def __build(self, directory):
        '''Return the root of a sub tree containing an arbitrary number of
        Nodes with keys representing all the files and folders in directory as
        File and Directory objects.'''
        dirNode = Node(Directory(directory, 0))
        dirSize = 0
        # Search for all files and folders within the directory
        for item in os.listdir(directory):
            itemPath = os.path.join(directory, item)
            itemSize = os.path.getsize(itemPath)
            # Check if item is a directory
            if os.path.isdir(itemPath):
                # Recursively obtain the Node and add it to the container of
                # the current Directory's Node.
                node = self.__build(itemPath)
                dirNode.add(node)
                dirSize += node.key.size
            else:
                # Create a File node and add it to the current Directory's Node
                node = Node(File(itemPath, itemSize))
                dirNode.add(node)
                dirSize += itemSize
        # Save new filesize to directory object
        dirNode.key.size = dirSize
        return dirNode

    def build(self, directory):
        '''Create a tree with the root associated with a Node with key
        Directory associated with directory and an arbitrary number of children
        Nodes with key associated with File and Directory objects.'''
        self.root = self.__build(directory)

    def getRoot(self):
        '''Return the root of the entire Treemap.'''
        return self.root
