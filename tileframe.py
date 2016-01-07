from PyQt4 import QtGui, QtCore
from treemap import Treemap


class TileFrame(QtGui.QFrame):
    ''''''

    def __init__(self, parentWindow):
        ''''''
        super(TileFrame, self).__init__(parentWindow)
        # TileFrame variables
        self.__treemap = None
        self.__borderCol = QtGui.QColor(0, 0, 0)
        self.__bgCol = QtGui.QColor(64, 64, 64)
        self.__txtCol = QtGui.QColor(38, 38, 38)
        self.__txtFont = QtGui.QFont('CopperBlack', 60, QtGui.QFont.Bold)
        self.__txt = "Visualizer"
        # Set strong policy for focusing keyboard events to Tileframe
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def __buildTiles(self, painter, node, size, location):
        ''''''
        borderRect = QtCore.QRect(location[0], location[1], size[0], size[1])
        # Shift the dimensions of the rectangle
        location[0] += 1
        location[1] += 1
        size[0] -= 2
        size[1] -= 2
        totalSize = max(float(node.key.size), 1)  # Prevent ZeroDivisionError
        for item in node.children:
            percent = item.key.size / totalSize
            itemArea = (size[0] * size[1]) * percent
            # Calculate dimensions of the rectangle
            if size[1] > size[0]:
                width = size[0]
                height = itemArea / width
                # Draw rectangle
                self.__drawRectangle(painter, item, [width, height], location)
                location[1] += height
            else:
                height = size[1]
                width = itemArea / height
                # Draw rectangle
                self.__drawRectangle(painter, item, [width, height], location)
                location[0] += width
        # Draw the border around the rectangle
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(self.__borderCol)
        painter.drawRect(borderRect)

    def __drawRectangle(self, painter, node, size, location):
        ''''''
        # If the node is associated with a colour
        if node.key.colour:
            rect = QtCore.QRect(location[0], location[1], size[0], size[1])
            # Obtain the file's colour and render the tile
            rgb = node.key.colour
            painter.fillRect(rect, QtGui.QColor(rgb[0], rgb[1], rgb[2]))
        # Recursively render the next level of tiles
        self.__buildTiles(painter, node, size, location[:])

    def screenshot(self, filename):
        ''''''
        QtGui.QPixmap.grabWindow(self.winId()).save(filename, 'png')

    def clearMap(self):
        ''''''
        self.__treemap = None

    def updateMap(self, directory):
        ''''''
        self.__treemap = Treemap()
        self.__treemap.build(directory)

    def paintEvent(self, event):
        ''''''
        painter = QtGui.QPainter(self)  # Used to draw on the frame
        # Clear all drawings on the GridFrame
        painter.eraseRect(0, 0, self.width(), self.height())
        if self.__treemap:
            # Set the initial conditions and render the Treemap
            size = [self.width(), self.height()]
            location = [0, 0]
            self.__buildTiles(painter, self.__treemap.getRoot(), size,
                              location)
        else:
            # Draw the default background
            painter.fillRect(0, 0, self.width(), self.height(), self.__bgCol)
            # Draw the default text
            painter.setPen(self.__txtCol)
            painter.setFont(self.__txtFont)
            painter.drawText(event.rect(), QtCore.Qt.AlignCenter, self.__txt)
