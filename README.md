# Summary

AI game player for a game called Teeko.

As you're probably aware, there are certain kinds of games that computers are very
good at, and others where even the best computers will routinely lose to the best human
players. The class of games for which we can predict the best move from any given
position (with enough computing power) is called Solved Games. Teeko is an example
of such a game, I will be implementing an AI player for it.

## How to play Teeko

Teeko is very simple:

It is a game between two players on a 5x5 board. Each player has four markers of
either red or black. Beginning with black, they take turns placing markers (the "drop
phase") until all markers are on the board, with the goal of getting four in a row
horizontally, vertically, or diagonally, or in a 2x2 box as shown above. If after the drop
phase neither player has won, they continue taking turns moving one marker at a time --
to an adjacent space only! (this includes diagonals, not just left, right, up, and down one
space.) -- until one player wins. Note, the game has no “wrap-around” similar to other
board games, so a player can not move off of the board or win using pieces on the other
side of the board.

## Win conditions summarized for Teeko:

```
● Four same colored markers in a row horizontally, vertically, or diagonally.
● Four same colored markers that form a 2x2 box.
```
## Program Specification

MAKE SURE TO USE PYTHON VERSION 3.10.

(You can check your python version by running python3 –version on the terminal)

### Make Move

The make_move(self, state) method begins with the current state of the board. It generates
the subtree of depth d under this state, create a heuristic
scoring function to evaluate the "leaves" at depth d (as you may not make it all the way
to a terminal state by depth d so these may still be internal nodes) and propagate those
scores back up to the current state, and select and return the best possible next move
using the minimax algorithm.

You may assume that your program is always the max player.

#### 1. Generate Successors

A successor function (e.g. succ(self, state) ) takes in a board state
and returns a list of the legal successors. During the drop phase, this simply means
adding a new piece of the current player's type to the board; during continued
gameplay, this means moving any one of the current player's pieces to an unoccupied
location on the board, adjacent to that piece.

Note: wrapping around the edge is NOT allowed when determining "adjacent" positions.

#### 2. Evaluate Successors

game_value(self, state) is a function to score
each of the successor states. A terminal state where the AI player wins should have
the maximal positive score (1), and a terminal state where the opponent wins should
have the minimal negative score (-1).

A heuristic_game_value(self, state) function is defined to evaluate non-terminal
states. This function should return some floating-point value between 1 and -1.

#### 3. Implement Minimax

```
● Defined a max_value(self, state, depth) function where the first call
will be max_value(self, curr_state, 0) and every subsequent
recursive call will increase the value of depth.
● When the depth counter reaches the tested depth limit OR it finds a
terminal state, it terminates the recursion.
```
The make_move() method is timed to see how
deep in the minimax tree you can explore in under five seconds. 
A value was picked that will safely terminate in under 5 seconds.