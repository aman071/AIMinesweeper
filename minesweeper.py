import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():                                                                                               #TO UPDATE ANY KNOWLEDGE, HAVE TO MAKE SENTENCE.
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells)==self.count:                                                                         #If count equal to len of sets, all are mines.
            return self.cells

        return set()                                                                                            #Otherwise we can't say anything for sure.

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:                                                                                       #If count is 0, all are safe.
            return self.cells

        return set()                                                                                            #Otherwise we can't say anything for sure.

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # self.cells.remove(cell)                                                                          #Would raise error if cell not present
        if cell in self.cells:
            self.cells.remove(cell)                                                                                 #Remove cell which is a mine
            self.count-=1                                                                                           #Update count for remaining set

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)                                                                                 #Can simply remove that cell. Count doesn't change.


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:                                                                      #Tell all other sentences that this is a mine. Addning new knowledge
            sentence.mark_mine(cell)

    def mark_safe(self, cell):                                                                               #Same as mark_mine function.
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    # def add_new(self):
    #     for sentence in self.knowledge:                                                                     #For out new knowledge
    #         # if len(sentence.cells) == 0:
    #         #     self.knowledge.remove(sentence)
    #         # else:
    #         new_safes = sentence.known_safes()
    #         new_mines = sentence.known_mines()

    #     return new_safes, new_mines

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print('Move made. In add_knowledge')
        self.moves_made.add(cell)                                   #1
        self.mark_safe(cell)                                        #2                                     #Will not add duplicates since it is a set.

        #Get neighboring cells
        count_mines=0
        neighbors = set()
        (row,column)=cell
        for i in range(row - 1, row + 2):                           #3a                                    #Get adjacent cells. For all cells 1 row above and below and 1 column left and right
            for j in range(column - 1, column + 2):
                if (i, j) == cell:                                                                         #Skip (row,column) cell
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    
                    if (i,j) in self.moves_made:                                                            #Not adding
                        continue

                    elif (i,j) in self.safes:                                                                 #Not adding
                        continue

                    elif (i,j) in self.mines:                                                                 #Not adding
                        count_mines+=1
                        continue

                    else:
                        neighbors.add((i, j))                                                                   #Getting list of neighbors


        new_know=Sentence(neighbors, count-count_mines)

        if new_know not in self.knowledge:
            self.knowledge.append(new_know)                        #3b

        new_safes=set()
        new_mines=set()                                            #4                                     #Get info about any new mines or safes

        for sentence in self.knowledge:                            #4
            new_safes_t = sentence.known_safes()
            new_mines_t = sentence.known_mines()
        
            if type(new_safes_t) is set:
                new_safes |= new_safes_t

            if type(new_mines_t) is set:
                new_mines |= new_mines_t

        for mine in new_mines:
            self.mark_mine(mine)

        for safe in new_safes:
            self.mark_safe(safe)

        inf = []
        prev_sentence = new_know
        for sentence in self.knowledge:                            #5
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

            elif prev_sentence == sentence:
                break

            elif prev_sentence.cells <= sentence.cells:                                                     #Inference resolution
                ce = sentence.cells - prev_sentence.cells
                co = sentence.count - prev_sentence.count

                inf.append(Sentence(ce, co))

            prev_sentence = sentence

        self.knowledge+=inf

        print('Finished adding knowledge')


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        print('Trying to make safe move')

        if len(self.safes)==0:
            return None

        for cell in self.safes:
            if cell not in self.moves_made:
                # self.moves_made.add(cell)                                                                  #IMPORTANT. SPENT AN HOUR FIGURING THIS OUT.
                print('Making safe move')
                return cell

        print('No safe moves')
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        for i in range(0,self.height):
            for j in range(0,self.width):
                cell=(i,j)

            if cell not in self.moves_made and cell not in self.mines:
                print("Making move")
                print(i,j)
                # self.mark_safe(cell)
                return cell
            
        return None
