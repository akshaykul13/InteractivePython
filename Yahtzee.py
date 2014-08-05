"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:            
            for item in outcomes:
                new_sequence = list(partial_sequence)                
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_sequences1(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:  
            print type(partial_sequence)
            temp_outcomes = list(outcomes)
            for val in partial_sequence:
                temp_outcomes.remove(val)
            #print partial_sequence
            temp_outcomes = tuple(temp_outcomes)
            for item in temp_outcomes:
                new_sequence = list(partial_sequence)                
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    score_1 = 0
    score_2 = 0
    score_3 = 0
    score_4 = 0
    score_5 = 0
    score_6 = 0
    max_score = 0
    for die_roll in hand:
        if die_roll == 1:
            score_1 += 1
            if score_1 > max_score:
                max_score = score_1
        elif die_roll == 2:
            score_2 += 2
            if score_2 > max_score:
                max_score = score_2
        elif die_roll == 3:
            score_3 += 3
            if score_3 > max_score:
                max_score = score_3
        elif die_roll == 4:
            score_4 += 4
            if score_4 > max_score:
                max_score = score_4
        elif die_roll == 5:
            score_5 += 5
            if score_5 > max_score:
                max_score = score_5
        elif die_roll == 6:
            score_6 += 6
            if score_6 > max_score:
                max_score = score_6
        
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """    
    outcomes = set([])    
    for val in range(num_die_sides):
        outcomes.add(val+1)
    #print outcomes
    length = num_free_dice
    seq_outcomes = gen_all_sequences(outcomes, length)
    final_score = 0
    for pos_outcome in seq_outcomes:
        #print pos_outcome
        hand = held_dice
        hand = hand + (pos_outcome)
        #print hand
        cur_score = score(hand)
        #print cur_score
        final_score += cur_score
    print float(final_score)/float(len(seq_outcomes)) 
    return float(final_score)/float(len(seq_outcomes))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    ans = set([()])
    ans.add(tuple(()))
    for num in range(len(hand)+1):
        length = num
        all_sequences = gen_all_sequences1(hand, length)
        sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
        #print sorted_sequences
        for outcome in sorted_sequences:
            #if hold_hand(outcome):
            ans.add(tuple(outcome))
    #print ans
    #print type(ans)
    return ans

def hold_hand(hand):
    """
    Method to check if the hand can be held or not
    """
    hold = True
    if len(hand) != 0:
        val = hand[0]
    for num in hand:
        if num != val:
            hold = False
            break
    return hold
    


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_value = 0
    req_hold = None
    for each_hold in all_holds:
        value = expected_value(each_hold, num_die_sides, len(hand) - len(each_hold))
        if value > max_value:
            max_value = value
            req_hold = each_hold
    print max_value
    print req_hold
    return (max_value, req_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    print score(hand)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()
#expected_value((2, 2), 6, 2)
#gen_all_holds((1,2)) 
#expected set([(), (1,)]) but received set([()])

#strategy((1,), 6)
#expected_value((3, 3), 8, 5) 
#expected (3.5, ()) but received (0.0, ())

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)                                    