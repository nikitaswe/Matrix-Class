import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    ############################# 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            det = self.g[0][0]
        else:
            det = self.g[0][0]*self.g[1][1] - self.g[0][1]*self.g[1][0]
        return det

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        return sum([self.g[i][i] for i in range(self.h)])


    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        inversed = zeroes(self.h, self.w)
        if self.h == 1:
            return 1/self.g[0][0]
        else:
            return 1.0 / self.determinant() * (self.trace() * identity(self.w) - self)
            

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        transposed = zeroes(self.w, self.h)
        for i in range(0, transposed.h):
            for j in range(0, transposed.w):
                transposed[i][j] = self.g[j][i]
        return transposed


    def is_square(self):
        return self.h == self.w
        

    def get_row(self, n):
        return self.g[n]
    

    def get_column(self, n):
        column = []
        for i in range(self.h):
            column.append(self.g[i][n])
        return column
    

    def dot_product(self, vector1, vector2):
        sum = 0
        for i in range(len(vector1)):
            sum += vector1[i]*vector2[i]
        return sum


    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        new_matrix = zeroes(self.h, self.w)
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")     
        for i in range(self.h):
            for j in range(self.w):
                new_matrix[i][j] = self.g[i][j] + other[i][j]
        return new_matrix

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        return Matrix([[-self.g[row][col] for row in range(self.h)] for col in range(self.w)])


    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be substracted if the dimensions are the same")     
        return (self + -other)


    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
                            
        if self.w != other.h:
            raise(ValueError, "Matrices can only be myltiplicated if m1 columns == m2 rows")     
                
        new_matrix = zeroes(self.h,other.w)
        
        for i in range(self.h):
            for j in range(other.w):
                new_matrix[i][j] = self.dot_product(self.get_row(i), other.get_column(j))
        return new_matrix
                

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        new_matrix = zeroes(self.h, self.w)
        if isinstance(other, numbers.Number):
            for i in range(self.h):
                for j in range(self.w):
                    new_matrix[i][j] = self.g[i][j] * other
        return new_matrix
        