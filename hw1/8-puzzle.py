
from __future__ import annotations
from dataclasses import dataclass, field
import heapq
from typing import Callable
from PrettyPrint import PrettyPrintTree


moves_available_from = {1: [2, 4], 
                        2: [1, 3, 5],
                        3: [2, 6],
                        4: [1, 5, 7],
                        5: [2, 4, 6, 8],
                        6: [3, 5, 9],
                        7: [4, 8],
                        8: [5, 7, 9],
                        9: [6, 8]}

def num_misplaced_tiles( state: list[ int] ) -> int:
    count = 0

    for position in range( 1, 10 ):
        if state[ position ] < 0:
            continue
        if state[ position ] != position:
            count += 1

    return count

def total_manhattan_distance( state: list[ int] ) -> int:
    total = 0

    for position in range( 1, 10 ):
        if state[ position ] < 0:
            continue
        
        curr_pos = position - 1
        desired_pos = state[ position ] - 1

        curr_pos_x = curr_pos % 3
        curr_pos_y = curr_pos // 3

        desired_pos_x = desired_pos % 3
        desired_pos_y = desired_pos // 3

        horizontal_dist = abs(desired_pos_x - curr_pos_x)
        vertical_dist = abs(desired_pos_y - curr_pos_y)

        manhattan_dist = vertical_dist + horizontal_dist
        total += manhattan_dist

    return total


@dataclass( order=True )
class TreeNode:

    estimated_cost: int
    heuristic_val: int = field( compare=False )
    cost_val: int = field( compare=False )
    board: list[ int ] = field( compare=False )

    parent: TreeNode = field( compare=False )
    children: list[ TreeNode ] = field( compare=False )

    explore_order: int = field( compare=False )


    def __init__( self, heuristic_val: int, cost_val: int, board: list[ int ] ):
        self.estimated_cost = heuristic_val + cost_val
        self.heuristic_val = heuristic_val
        self.cost_val = cost_val
        self.board = board
        self.parent = None
        self.children = []
        self.explore_order = 0

    def get_available_moves( self ) -> list[ list[ int ] ]:
        possible_new_states: list[ list[ int ] ] = []
        blank_position: int = self.board[ 0 ]
        possible_moves: list[ int ] = moves_available_from[ blank_position ]

        for move in possible_moves:
            new_board: list[ int ] = self.board.copy()

            new_board[ blank_position ] = new_board[ move ]
            new_board[ move ] = -1
            new_board[ 0 ] = move

            possible_new_states.append( new_board )

        return possible_new_states

    def __str__(self) -> str:

        str_board: list[ str ] = [ str( x ) if x > 0 else "_" for x in self.board ] 
        res = ""
        res += f"{str_board[ 1 ]} {str_board[ 2 ]} {str_board[ 3 ]} [{self.explore_order}]\n"
        res += f"{str_board[ 4 ]} {str_board[ 5 ]} {str_board[ 6 ]}\n"
        res += f"{str_board[ 7 ]} {str_board[ 8 ]} {str_board[ 9 ]} ({self.heuristic_val})"

        return res



# [ 1 2 3 ]
# [ 4 5 6 ]
# [ 7 8 9 ]

def a_star(start_state: list[int], heuristic_function: Callable[[list[int]], int]) -> list[int]:

    start_cost = 0
    start_heuristic = heuristic_function( start_state )

    root = TreeNode( start_heuristic, start_cost, start_state )
    root.parent = TreeNode( 0, 0, [ 9, 1, 2, 3, 4, 5, 6, 7, 8, -1 ] )

    heap = [ root ]

    explore_order = 1
    root.explore_order = explore_order

    while heap:

        curr_node = heapq.heappop( heap )


        
        curr_node.explore_order = explore_order
        explore_order += 1

        curr_node.parent.children.append( curr_node )

        if curr_node.cost_val > 4:
            break
        # print(curr_node)

        for new_board in curr_node.get_available_moves():

            cost_val = curr_node.cost_val + 1
            heuristic_val = heuristic_function( new_board )

            new_node = TreeNode( heuristic_val, cost_val, new_board )
            new_node.parent = curr_node
            
            heapq.heappush( heap, new_node )

    pt = PrettyPrintTree( lambda treenode: treenode.children, lambda treenode: str(treenode), orientation=PrettyPrintTree.Vertical, return_instead_of_print=False )
    pt( root )

    # tree_str = pt( root )
    # f = open( "./tree.txt", "w" )
    # f.write( tree_str ) 
    # f.close()


start_state = [5, 7, 2, 4, 5, -1, 6, 8, 3, 1] # Index 0 contains the position of the empty space, index 1 to 9 contains the tile in the corresponding position

a_star( start_state, total_manhattan_distance )
# start_cost = 0
# start_heuristic = num_misplaced_tiles( start_state )
# start_estimated_cost = 0 + num_misplaced_tiles( start_state )

# root = TreeNode( start_estimated_cost, start_heuristic, start_cost, start_state )
# print( root )