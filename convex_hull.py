from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    def getXCoord(self, point):
        return point.x()

    def getRightMostPoint(self, polygon):
        pointIndex = 0
        for i in range(len(polygon)):
            if polygon[i].x1() > polygon[pointIndex].x1():
                pointIndex = i
        return pointIndex

    def getLeftMostPoint(self, polygon):
        pointIndex = 0
        for i in range(len(polygon)):
            if polygon[i].x1() < polygon[pointIndex].x1():
                pointIndex = i
        return pointIndex

    def isUpperTangent(self, tangent, hull):
        for line in hull:
            yvalue = (((tangent.y2() - tangent.y1()) / (tangent.x2() - tangent.x1())) * (
                    line.x1() - tangent.x1())) + tangent.y1()
            if round(yvalue, 6) < round(line.y1(), 6):
                return False
        return True

    def isLowerTangent(self, tangent, hull):
        for line in hull:
            yvalue = (((tangent.y2() - tangent.y1()) / (tangent.x2() - tangent.x1())) * (
                    line.x1() - tangent.x1())) + tangent.y1()
            if round(yvalue, 6) > round(line.y1(), 6):
                return False
        return True

    def merge(self, lHull, rHull):

        upperlHullIndex = lowerlHullIndex = self.getRightMostPoint(lHull)
        upperrHullIndex = lowerrHullIndex = self.getLeftMostPoint(rHull)
        findingTangent = True
        while (findingTangent):
            tangent = QLineF(lHull[upperlHullIndex].p1(), rHull[upperrHullIndex].p1())
            leftChange = False
            rightChange = False
            #self.blinkTangent([tangent],GREEN)
            if not(self.isUpperTangent(tangent, lHull)):  # lHullPoint move counter clockwise
                leftChange = True
                if upperlHullIndex == 0:
                    upperlHullIndex = len(lHull)-1
                else:
                    upperlHullIndex = upperlHullIndex - 1
            elif not(self.isUpperTangent(tangent, rHull)):  # rHullPoint move clockwise
                rightChange = True
                if upperrHullIndex == len(rHull)-1:
                    upperrHullIndex = 0
                else:
                    upperrHullIndex = upperrHullIndex + 1

            findingTangent = (leftChange or rightChange)
        upperTangent = QLineF(lHull[upperlHullIndex].p1(), rHull[upperrHullIndex].p1())
        #self.blinkTangent([upperTangent], GREEN)
        #self.showTangent([upperTangent], GREEN)

        findingTangent = True
        while (findingTangent):
            tangent = QLineF(lHull[lowerlHullIndex].p1(), rHull[lowerrHullIndex].p1())
            leftChange = False
            rightChange = False
            #self.blinkTangent([tangent], GREEN)
            if not (self.isLowerTangent(tangent, lHull)):  # lHullPoint move counter clockwise
                leftChange = True
                if lowerlHullIndex == len(lHull)-1:
                    lowerlHullIndex = 0
                else:
                    lowerlHullIndex = lowerlHullIndex + 1
            elif not (self.isLowerTangent(tangent, rHull)):  # rHullPoint move clockwise
                rightChange = True
                if lowerrHullIndex == 0:
                    lowerrHullIndex = len(rHull)-1
                else:
                    lowerrHullIndex = lowerrHullIndex - 1
            findingTangent = leftChange or rightChange
        lowerTangent = QLineF(rHull[lowerrHullIndex].p1(), lHull[lowerlHullIndex].p1())
        #self.blinkTangent([lowerTangent], GREEN)
        #self.showTangent([lowerTangent], GREEN)

        i = lowerlHullIndex
        leftHalf = []
        while i != upperlHullIndex:
            leftHalf.append(lHull[i])
            i = (i+1) % len(lHull)
        i = upperrHullIndex
        rightHalf = []
        while i != lowerrHullIndex:
            rightHalf.append(rHull[i])
            i = (i+1) % len(rHull)
        # if(lowerlHullIndex > upperlHullIndex):
        #     leftHalf = lHull[lowerlHullIndex:len(lHull)]
        #     leftHalf +=(lHull[0:upperlHullIndex])
        # else:
        #     leftHalf = lHull[lowerlHullIndex:upperlHullIndex]
        #
        # if (upperrHullIndex > lowerrHullIndex):
        #     rightHalf = rHull[upperrHullIndex:len(rHull)]
        #     rightHalf +=(rHull[0:lowerrHullIndex])
        # else:
        #     rightHalf = rHull[upperrHullIndex:lowerrHullIndex]

        mergedHull = [upperTangent] + rightHalf + [lowerTangent] + leftHalf
        #TODO seed:11  points:6 not clockwise

        #self.showHull(mergedHull, RED)
        return mergedHull

    def convexHull(self, points):
        if len(points) == 3:
            if(points[1].y() > points[2].y()):
                return [QLineF(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
            else:
                return [QLineF(points[0],points[2]), QLineF(points[2], points[1]), QLineF(points[1], points[0])]
        if len(points) <= 2:
            return [QLineF(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]

        leftPoints = points[0:int(len(points) / 2) + (len(points) % 2)]
        rightPoints = points[int(len(points) / 2) + (len(points) % 2):len(points)]
        leftHull = self.convexHull(leftPoints)
        #self.showHull(leftHull, RED)
        rightHull = self.convexHull(rightPoints)

        #self.showHull(rightHull, RED)
        return self.merge(leftHull, rightHull)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        points.sort(key=self.getXCoord)
        # TODO: SORT THE POINTS BY INCREASING X-VALUE
        t2 = time.time()
        print('Time Elapsed (Sort points): {:3.3f} sec'.format(t2 - t1))

        t3 = time.time()
        # this is a dummy polygon of the first 3 unsorted points
        # polygon = [QLineF(points[i], points[(i + 1) % 2]) for i in range(2)]
        polygon = self.convexHull(points)
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
