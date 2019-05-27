For this assignment we have used, MiniMax algorithm. 
This algorithm creates all possible moves till a certain depth and then selects the best possible move with a definite heuristic.

The minimax algorithm works by simulating gameplay where we want to maximise our profit and the opponent wants to minimize the offering to us. 
Hence, we use a heuristic such that, we want to increase the heuristic and the opponent chooses the heuristic value which is least in value. 
We start our value, ie alpha with -infinity, which is the least value and the opponent starts the game with the max value ie +infinity. 
And we keep checking for each valid next move in the recursion and see what the heuristic value is.
If it is greater than the current heuristic saved, then we replace it with the new one. 
Hence we get the most optimized result till a certain depth.

Our program works by the following points:
Parse the game move sent by the server, and place the move to the board. 
Update the next set of possible moves.
Next, we simulate the alpha-beta by deep copying the state of the game and play the game with the given heuristic 
and get the maximum profitable state and return and play it.

We have implemented the following heuristic (We are X and opponent is O) :- 
All the following conditions will be checked row-wise, column-wise and both diagonally.
1. Three In A Row: When we have the value as 3 X, we get 1 as the heuristic value. 
| X | X | X |
| _ | _ | _ |
| _ | _ | _ |

2. Two X and one O:  When we have 2 X and the opponent has -1 O in the same row/column/diagonal.
| X | X | 0 |
| _ | _ | _ |
| _ | _ | _ |

3. Fork: When we have 3 X in corners we have a 'Fork' situation with one empty cell in between them. we will give 1 point to heuristic to get the fork position. Below is the illustration for the fork position. Fork position is advantageous as it gives us 2 winnning positions in same board.
| X | _ | X |
| _ | _ | _ |
| _ | _ | X | 

4. Play centre: When the centre is not played, we give it 1 heuristic point. (5th tile)

5. Blocking opposite corner: When the opposite corner is empty, we grant 1 point to the heuristic.
| O | _ | _ |
| _ | _ | _ |
| _ | _ | _ | <- one possible point to play

6. Play empty corner: If any of the corners is empty, we give 1 point to the heuristic.

7. Two X and one empty:  When we have 2 X and the next in the same row/column/diagonal is empty.
| X | X | _ | <- possible position to play
| _ | _ | _ |
| _ | _ | _ |

8. Create Fork: When we have 2 corners occupied and 1 of the other 2 corners are unoccupied, we can get into a Fork position.
| X | _ | X |
| _ | _ | _ |
| _ | _ | X | <-one  possible point to create a fork

9. Block fork: When we block a opponent's fork formation , we grant 1 point to the heuristic.
| 0 | _ | 0 |
| _ | _ | _ |
| _ | _ | _ | <-one  possible point to stop a fork

10. Block winning psoition of opponent: If the opponent is present in 2 places in a line(row/column/diagonal), with the 3rd position empty, we try to block opponent's move by occupying that 3rd position.

| O | X | O |
| _ | _ | _ |
| _ | _ | _ | 

Moves leading us to winning position-> (1, 3, 7, 8)
Moves that block opponent from winning -> (5, 9, 10)
Moves that bring little benefit -> (2, 4, 6)

We assign weights to all these possible heuristic values and subtract the values with the opponent’s heuristic value which gives us our actual heuristic value (with consideration of the opponent).

