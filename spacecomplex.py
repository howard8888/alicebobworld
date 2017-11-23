# -*- coding:utf-8 -*- 
#
# implementation of Alice and Bob playing space complexity games
#
# Note : This code is based on a segment of the work of Garg and Schneider 2017, 
#         abstract reproduced below from the preprint server:
#         https://arxiv.org/abs/1710.02898
'''
The space complexity of mirror games

Sumegha Garg, Jon Schneider
(Submitted on 8 Oct 2017)
We consider a simple streaming game between two players Alice and Bob, which we call the mirror game. In this game, Alice and Bob take turns saying numbers belonging to the set {1,2,…,2N}. A player loses if they repeat a number that has already been said. Bob, who goes second, has a very simple (and memoryless) strategy to avoid losing: whenever Alice says x, respond with 2N+1−x. The question is: does Alice have a similarly simple strategy to win that avoids remembering all the numbers said by Bob? 
The answer is no. We prove a linear lower bound on the space complexity of any deterministic winning strategy of Alice. Interestingly, this follows as a consequence of the Eventown-Oddtown theorem from extremal combinatorics. We additionally demonstrate a randomized strategy for Alice that wins with high probability that requires only O~(N−−√) space (provided that Alice has access to a random matching on K2N). 
We also investigate lower bounds for a generalized mirror game where Alice and Bob alternate saying 1 number and b numbers each turn (respectively). When 1+b is a prime, our linear lower bounds continue to hold, but when 1+b is composite, we show that the existence of a o(N) space strategy for Bob implies the existence of exponential-sized matching vector families over ZN1+b.
Comments:	13 pages
Subjects:	Computational Complexity (cs.CC); Discrete Mathematics (cs.DM)
Cite as:	arXiv:1710.02898 [cs.CC]
'''


#imports
import random 
import time 
import platform
from collections import namedtuple
try:
    import psutil
except:
    print '\nConsider installing psutil library to get time complexity results.'
    print  '(It is not included in Python Standard Library but readily available via pypi/psutil or via anaconda distribution.)/n'
  
  
#global variables 
'''numbers -- list or set holding numbers chosen by players
   GIT_SYNCH -- used to ensure Git is synchronizing latest version or date of the code
   '''
numbers =[]
GIT_SYNCH=152

class Numbers(object):
    ''' Initializes and maintains array or set holding chosen numbers by players.
        Uses decorator to allow static methods for convenience of use. 
        In future version convert this class to module but for moment as is.
        Key variables:
          gamesize -- highest number which players may guess which is same as maximum number of turns
          TIMES_DEFAULT -- default value for the number of times run a game in batch mode, times being chosen value
          guess_list -- guess algos bob and alice are allowed to choose from for their game
          bp -- [bob algo, alice algo, n max number, times ], if 0's then interactive parm input
          batch_array -- if times >1 then will stores results of each game of batch run in batch_array
          time_array -- stores time of run (whether batch or interactive)/n for each interactive or batch run
          no_ties (and NO_TIES_DEFAULT) -- if 1 then this means no ties allowed -- if player cannot add a valid number then loses (if 0 then if all numbers used up, is a tie)
        Program originally written for interactive mode and then batch mode added and then multiple times (ie, run multiple games) added
        The critical parameters [bob algo, alice algo, n max number, times ] are used as follows depending if
        running in batch OR interactive mode:
            bob algo:  self.guess_algo = self.bp.bob  OR  = Numbers.choose.guess_algo(self.name) (used with Bob object)
            alice algo:  self.guess_algo = self.bp.alice  OR  = Numbers.choose.guess_algo(self.name) (used with Alice object)
            n:  Numbers.gamesize = Numbers.bp.n  OR =  Numbers.choose_gamesize()
            times:  Numbers.bp.times   ('times' only used in batch mode, no interactive ability to enter times) 
                ('times' refers to how many games run one after another with given parameters)
            
        '''
    
    gamesize = 0  
    GAMESIZE_DEFAULT =11
    TIMES_DEFAULT=1
    guess_list = [1,2,3,4,5,6,7,8,9,10,11]   
    Batchy=namedtuple('namedtuple_for_batch_parms','bob alice n times')
    bp=Batchy._make([0,0,0,0])
    #previous code: 'batch_parameters' used instead of 'bp'; prior to that: 'batch_parameters' was a list not a namedtuple
    batch_array=[] 
    time_array=[]
    NO_TIES_DEFAULT=1
    no_ties=NO_TIES_DEFAULT
    def __init__(self): 
        pass #TODO: will write later as req'd

   
    def __str__(self):
        return 'Numbers Class exists'
    
    @staticmethod
    def welcome():
        '''print statements about welcome to the game
        '''
        print """\n\n
        Welcome to Data Negotiation World
        
        Imagine you are in a world where everything functions by way of
        communication or negotiation between two parties -- we can call
        them Bob and Alice. Even machines are built in this fashion -- 
        there is a communication back and forth between the user and the
        machine, in a Bob -- Alice fashion. Everything in this world -- 
        people, the rules of society, machines, even many biological mechanisms
        function like this.
        
        The problem is that neither 'Bob' nor 'Alice' have infinite memories
        or infinite time to assist with the communication they must produce
        in reponse to a communication and usually many previous communications
        they have received.
        
        Let's explore the properties of this 'Data Negotiation World' with a
        game of space complexity. Bob and Alice can use different strategies,
        including the mirror strategy discussed in the comments of this code,
        and have access to different amounts of computional cycles ('time 
        complexity') and different amounts of memory space ('space
        complexity').
        
        In this game of space complexity, Alice and Bob will take turns
        saying a number (positive integers are used).
        If one of the players says a number which has already been said,
        then that player loses.
        
        Your role is as referee, setting the rules (ie, algorithms and 
        parameters) which Alice and Bob can use.
        
        Note: Alice always moves first.
        Note: Default mode is that no ties are allowed -- if any player
        makes a wrong guess for any reason, including all the numbers
        being used up, then that player loses. However, user configurable so
        that ties can be allowed to occur if all numbers used up and no 
        player has lost yet.\n\n"""
        
    @staticmethod
    def choose_gamesize():
        '''get value of gamesize, ie, n for length of list, ie, successful number
        of turns
      Note: Default mode is that no ties are allowed -- if any player
        cannot make a valid guess for any reason, including all the numbers
        being used up, then that player loses. However, this method allows
        user to change NO_TIES to 0, ie, off, so that ties are indeed allowed
        to occur if all numbers are used up and no player has lost yet.
        '''
        
        print '''\n\n           Ties vs No_Ties
        ------------------------
        Default mode when program starts is that no ties are allowed -- 
        if any player cannot make a valid guess for any reason, including
        all the numbers being used up, then that player loses. However,
        you can change this setting whenever you want. If you allow ties,
        then if all the numbers are used up (ie, guessed) and no player has
        lost yet, then this will be considered a tie.
        '''
        if Numbers.no_ties ==1 :
                    print 'At present ties are not allowed.'
        else:
                    print 'At present ties are allowed -- if all numbers used up, then this will be tie'
        try:
                    x=raw_input('Do you want to change (ie, toggle) if ties are allowed/not allowed [y,yes,n,no,ENTER for no]: ')
                    if x=='y' or x=='yes':
                        if Numbers.no_ties==0:
                            Numbers.no_ties=1
                        else:
                            Numbers.no_ties=0
                        print '\nTies allowed status toggled. Status now is( 0 - ties allowed, 1 - not allowed): {}'.format(Numbers.no_ties)
                    else:
                        print '\nTies allowed status not changed. Status remains( 0 - ties allowed, 1 - not allowed): {}'.format(Numbers.no_ties)                   
        except:
                    print '\nTies allowed status not changed. Status remains( 0 - ties allowed, 1 - not allowed): {}'.format(Numbers.no_ties)

        print '\n (highest integer allowed)'
        print '---------------------------'
        try:
            Numbers.gamesize=abs(int(raw_input('Highest integer players can say? [default ~11]: ')))
        except:
            print 'Default value of {} will be used'.format(Numbers.GAMESIZE_DEFAULT)
            Numbers.gamesize= Numbers.GAMESIZE_DEFAULT
        if Numbers.gamesize <2:
            Numbers.gamesize = 2 
        print 'This game will allow the players to choose numbers 1 - {}.\n'.format(Numbers.gamesize)
        time.sleep(2)
        return Numbers.gamesize
    
    @staticmethod
    def choose_guess_algo(name):
        '''print statements plus user choice of which algorithm a player
        should use'''
        print '{}'.format(name)
        print '-------'
        print 'You need to choose which algorithm {} should use for '.format(name) 
        print 'choosing a number to say. Available selections at present include:\n'
        print """
        1.  Random guessing,unlimited space & time until valid guess [default]
        2.  Mirror strategy,0 memory spaces, n forced even
        3.  Random guessing,0 memory spaces to check 0 previous guesses []
        4.  Random guessing,1 memory space to check last guess [n-1]
        5.  Random guessing,3 memory spaces to check 3 last guesses [n-1,2,3]
        6.  Guess 1 less than opponent\'s guess, 1 memory space [n-1]
        7.  Guess 1 less than opponent\'s guess, 2 memory spaces [n-1,3]
        8.  Code your own algo here (currently just returns a 1 as a guess)
        9.  Guess 1 more than opponent\'s guess, 1 memory space [n-1]
        10. Guess 1 more than opponent\'s guess, 2 memory spaces [n-1,2]
        11. Guess 1 more, 2 mem spaces [n-1,2],new algo max/used value guess
        12. Future: Random guess,3 mem spaces to check first 3 guesses
        13. Future: Random guess,3 mem spaces to check 3 random guesses
        14. Future: Random guess,3 mem spaces to most frequent used nos"""
        
        while True:
            try:
                guess_algo=int(raw_input('Please select what algorithm to use [default algo 1]: '))
            except:
                return 1 
            else:
                if (not(guess_algo in  Numbers.guess_list)):
                    return 1 
                else:
                    return guess_algo 
    
    @staticmethod
    def add(choice,name):
        '''A player's guess or 'choice' is sent to this function which appends it to the list numbers
        assuming the guessed number does not already exist in the list numbers. If the guess already
        exists then a -1 is returned and it is not appended vs +1 return for successful appending the number.'''
        if choice in numbers:
            print '{}\'s guess is {} which unfortunately already exists, thus {} loses.'.format(name,choice,name)
            return -1
        if (type(choice) is int) and (choice<=Numbers.gamesize) and (choice>0):
            numbers.append(choice)
            return +1
        else: 
        #automatic guesses generated internally and thus always valid numbers but in case allow manual guessing in future
            print '{}\'s manual guess is {} which is not a valid number, thus {} loses.'.format(name,choice,name)
            return -1
    
    @staticmethod
    def batch_input(rawinput_aboutplayingagain):
        '''allow input of batch run paraemeters and validations of
        parameters --at end of game can enter y,n,batch,'1,2',etc
        return [bob algo, alice algo, n, times ] if valid,
        return [0,0,0,0] if not valid
        Note: If [0,0,0,0] returned than this will indicate for next game
        to ask user to choose various parameters rather than automatic batch run
        (In automatic batch run parameters are specified in variable bp
        bp.bob (algo), bp.alice (algo), n (highest number), times (how many games to run) )
        Note: Here we are using the existing code which was written for 
        batch_parameters (since become namedtuple bp) as a list but after
        return [] array it will be converted to bp namedtuple.'''
        a = rawinput_aboutplayingagain 
        if a[0]=='g' or a =='version':
           print '\n\n\n\nInternal version number or date to make sure Git is synchronized: {}'.format(GIT_SYNCH)
           time.sleep(4)
           return [0,0,0,0]            
        if a[0] in ['0','1','2','3','4','5','6','7','8','9']:
            try:
                q=map(int, a.split(','))
            except:
                print 'Wrong input format -- will run again as non-batch run.\n'
                time.sleep(4)
                return [0,0,0,0]   
        else:
            print '\nBatch runs allow full and semi-automated running'
            print 'of the game simulations, including multiple runs.' 
            print 'You can specify [Bob strategy, Alice strategy],'
            print 'eg, enter "1,5" for Bob to use algo1 and Alice algo5'
            print 'in which case defaults of n={} and runs={} time(s) will '.format(Numbers.GAMESIZE_DEFAULT, Numbers.TIMES_DEFAULT)
            print 'be used, or you can specify everything,eg, "1,5,100,10" '
            print 'for Bob algo1, Alice algo5, guess 1-100, run 10 times'
            print 'Note:Alice always moves first'
            print 'Note: Go to interactive mode to change the TIES or NO_TIES mode,' 
            print  'ie, doe we allow a tie if all numbers used up, or if a player cannot'
            print 'make a valid guess for any reason, then that player loses.\n'
            print 'Pending feature: Re-runs everything a second time but can guess n+1 numbers'
            print ' this time so that runs with both odd and even maximum number of numbers'
            print ' are experienced. This feature automatically occurs.'
            print 'Pending feature: Enter "9999" and runs all the algos against each'
            print ' other n=11 (odd) and n=12 (even) each combo run 20 times, ie,'
            print ' if 15 algos then will generate matrix results 15x15 algos x2(odd/even).'
            try:
                q=map(int,raw_input('Enter: Bob algo, Alice algo, highest int, times run : ').split(','))
            except:
                print 'Wrong input format -- will run again as non-batch run.\n'
                time.sleep(4)
                return [0,0,0,0]
        if len(q) <2 or len(q)>4:
                if q==[9999]:  #run all algos against each other n odd/even
                    print 'Generate all algos x all algos matrix of results not available yet.'
                else:
                    print 'Too few or too many options -- will run again as non-batch run.\n'
                time.sleep(4)
                return [0,0,0,0]
        if len(q)==2:
            q.append(Numbers.GAMESIZE_DEFAULT)  #need to set n q[2] and q[3]
            q.append(Numbers.TIMES_DEFAULT)  
        if len(q)==3:
            q.append(Numbers.TIMES_DEFAULT)  #need to set q[3]
        if q[0]<0 or q[1]<0 or q[2]<0 or q[3]<0:
            print 'Negative integer  -- will run again as non-batch run.\n'
            time.sleep(4)
            return [0,0,0,0]
        if (q[0] not in Numbers.guess_list) or (q[1] not in Numbers.guess_list):
            print 'Wrong algo format -- will run again as non-batch run.\n'
            time.sleep(4)
            return [0,0,0,0]
        if  q[2]>10000:
            print  'Over batch mode allowed guess range (n) of 10,000, thus n=10,0000'
            time.sleep(4)
            q[2]=10000
        if  q[3]>10000:
            print  'Over batch mode allowed run range (times) of 10,000, thus times=10,0000'
            time.sleep(4)
            q[3]=10000
        if  q[3]==1:
            print  'Times==1 automatically changed to Times==0, ie, runs once and zero repeats.'
            time.sleep(4)
            q[3]=0
        return q
    
    @staticmethod
    def erase():
        '''Batch parameters reset to [0,0,0,0] for next game selection
        numbers, batch_array also erased'''
        del numbers[:]
        del Numbers.batch_array[:]
        Batchy=namedtuple('namedtuple_for_batch_parms','bob alice n times')
        Numbers.bp=Batchy._make([0,0,0,0])

     
    @staticmethod 
    def display_analysis():
        '''Analysis of the moves of the game which just occurred.
        Note: Some extra copies of numbers guessed by players in various
        formats to allow easy present and future analysis of data.'''
        #different representations of 'numbers'
        #copydict= {posn:guess for posn,guess in enumerate(numbers)}
        #print out lists of moves of games which occurred
        print 'Numbers already chosen (as actual list) (Alice is first move): {} '.format(numbers)
        if  (1.0*len(numbers)/Numbers.gamesize)==1:
            print 'Numbers already chosen (as sorted list): 1 - {} inclusive'.format(Numbers.gamesize)
        else:
           copysortedlist = sorted(numbers) 
           print 'Numbers already chosen (as sorted list): {} '.format(copysortedlist)
       # print 'Same information as dictionary of the original list: {}'.format(copydict)
        #analysis of these moves
        print 'Average guess value was ~ {}'.format(sum(numbers)/len(numbers))
        print '\n\n' 
    
    @staticmethod
    def batch_game_summary(Bob_text,Alice_text):
        '''Summary of results of multiple game runs of given parameters'''
        print '\nBatch Run Summary:\n------------------'
        print 'Batch parameters: {}  {}  {}  {}'.format(Numbers.bp.bob,Numbers.bp.alice,Numbers.gamesize,Numbers.bp.times )
        print 'Each game allows guesses from 1 - {}. Game was run {} times.'.format(Numbers.gamesize,Numbers.bp.times)
        print " Alice -- goes first -- algo #{} -- {}".format(Numbers.bp.bob,Bob_text)
        print " Bob -- goes second -- algo #{} -- {}".format(Numbers.bp.alice,Alice_text)
        if Numbers.no_ties == 1:
            print "  No ties were allowed (when a player guesses an already chosen number, that player loses, even if no more unchosen numbers exist"
        else:
            print "  Ties were allowed -- if no player has lost and all the numbers have been chosen already, then this is considered a tie"
        print 'Results of runs(+1 Bob won, 0 tie, -1 Alice won): {}\n'.format(Numbers.batch_array)
        total_score=0
        Bob_win=0
        Alice_win=0
        for i in range(len(Numbers.batch_array)):
            total_score+=Numbers.batch_array[i]
            if Numbers.batch_array[i]>0:
                Bob_win+=1
            if Numbers.batch_array[i]<0:
                Alice_win+=1
        print 'Total score {} -- Bob wins: {}, Alice wins: {}, ties: {}'.format(total_score,Bob_win,Alice_win,Numbers.bp.times-Bob_win-Alice_win)
        if total_score > 0:
            print ' -- Bob wins {:0.1f}% of games vs. Alice winning {:0.1f}% of games\n\n'.format(100.0*Bob_win/Numbers.bp.times, 100.0*Alice_win/Numbers.bp.times)
        elif total_score <0:
            print ' -- Alice wins {:0.1f}% of games vs. Bob winning {:0.1f}% of games\n\n'.format(100.0*Alice_win/Numbers.bp.times, 100.0*Bob_win/Numbers.bp.times)
        else:
            print ' -- Tie between Bob and Alice with both of them each winning {:0.1f}% of games, with rest ties\n\n'.format(100.0*Bob_win/Numbers.bp.times)
    
    @staticmethod
    def time_complexity_analysis(start_time,end_time):
        '''Summary of time results for the game runs'''
        map(Numbers.time_array.append,  ['n',Numbers.gamesize, 'runs',Numbers.bp.times, 'secs/run/n'])
        print 'Time for above run or batch runs was:  {:.5f} seconds'.format(end_time-start_time)
        if Numbers.bp.times != 0:
            print '  Time per run:  {:.6f} seconds'.format((end_time-start_time)/Numbers.bp.times)
            print '  Time per run per range of guess (n={}):  {:.6f} seconds/all possible guesses'.format(   Numbers.gamesize,  ((end_time-start_time)/Numbers.bp.times)/Numbers.gamesize   )
            Numbers.time_array.append(  round(((end_time-start_time)/Numbers.bp.times)/Numbers.gamesize,5)          )
        else:
           print '  Time for above run per range of guess (n={}): {:.5f} seconds/all possible guesses'.format(Numbers.gamesize, (end_time-start_time)/Numbers.gamesize)
           Numbers.time_array.append ( round((end_time-start_time)/Numbers.gamesize ,5))
        print 'List of all batches/single runs this session, showing parameters & seconds/each run/n to assist in time complexity analysis:\n', Numbers.time_array
        times_only=[]
        for i in range(0, len(Numbers.time_array)):
            if (i+1)%10==0 :
                times_only.append(Numbers.time_array[i])
        print 'List of all batches/single runs this session, showing only seconds/each run/ n : {}'.format(times_only)
        ave = sum(times_only)/len(times_only)
        print  'Average seconds/each run/n for this session: {}'.format(ave)
        star_times=[]
        for i in range(0,len(times_only)):
            if  abs(times_only[i] - ave) >  (.30*ave):
                star_times.append('*')
            star_times.append(times_only[i])
        print 'List of all batches/single runs this session, with flag of seconds/each run/n > or < 30% of average : {}'.format(star_times) 
        print '\nCPU used: {}'.format(platform.processor())
        try:
            print 'Memory used: {}'.format(psutil.virtual_memory())
            print 'CPU hardware cores: {}'.format(psutil.cpu_count(logical=False))
            print 'Logical CPUs: {}'.format(psutil.cpu_count())
        except:
            print 'Memory & CPU characteristics: requires installation of psutil library'
        print '\n-------------------------------------------------------\n\n'
        
        
class Player(object):
    '''Player class holds some of the data structures and methods that the players Bob and Alice (and other players
    if so desired) use in guessing numbers that each of them have said. Some of the data structures and methods also
    held in the largely statically typed class Numbers.
         Note: Some processing of batch commands appears less elegant than should below as batch processing
        was added on afterwards in later development.
         Overview of important variables:
        name -- will be Bob or Alice now, but can be other name in future use
            note: if add another name in future then bp must be appropriately adjusted
        bp -- [bob algo,alice algo,n,times], if 0's then do interactive input
            remember -- bob is 0 index, alice is 1 index with regard to their algos
        '''
    
    def __init__(self, name,bp):
        self.name = name 
        self.bp = bp  
        if self.bp.bob == 0: 
            self.guess_algo= Numbers.choose_guess_algo(self.name) 
        else: 
            if self.name == 'Bob': 
                self.guess_algo=self.bp.bob 
            else:
                self.guess_algo=self.bp.alice
        map(Numbers.time_array.append, [self.name, self.guess_algo])
        if self.guess_algo==2:
             if Numbers.gamesize%2 != 0:
                Numbers.gamesize+=1
                print 'Mirror Strategy guess algo requires even number of possible guesses.'
                print 'Maximum number of guesses increased to {}.'.format(Numbers.gamesize)
        print '\nThe player with name {} now exists and will use guess algorithm # {}'.format(name,self.guess_algo)
        if  Numbers.bp.times == 0:
            print '(Guesses must range from 1 - {}. The game will run only one time until there is a tie or win/loss.)\n'.format(Numbers.gamesize)
        else:
            print '(Guesses must range from 1 - {}. The game will run (ie, repeat) {} times over and over again in total using these parameters.)\n'.format(Numbers.gamesize, Numbers.bp.times)
        time.sleep(4)
      
    def guess1(self):
        '''random guessing with unlimited space and time constraints
        '''
        while True:
            x= random.randint(1,Numbers.gamesize)
            if not x in numbers:    
                return x
    
    def guess2(self):
        ''' Mirror strategy,0 memory spaces
       Requires 2N (ie, even n) maximum value, thus Numbers.gamesize has
       been incremented to an even value if it was chosen as odd.
       
       "The space complexity of mirror games -- Sumegha Garg, Jon Schneider
        (Submitted on 8 Oct 2017)
        We consider a simple streaming game between two players Alice and Bob, which we call the mirror game. In this game, Alice and Bob take turns saying numbers belonging to the set {1,2,…,2N}. A player loses if they repeat a number that has already been said. Bob, who goes second, has a very simple (and memoryless) strategy to avoid losing: whenever Alice says x, respond with 2N+1−x. The question is: does Alice have a similarly simple strategy to win that avoids remembering all the numbers said by Bob?....."
        '''
        if  len(numbers)>0:
            #if Alice chooses x, Bob chooses 2N (ie,even n)+1-x 
            return Numbers.gamesize + 1 -numbers[-1]
        else:
            print "**Mirror Strategy not intended to be first move of the game**"
            return Numbers.gamesize
        
    def guess3(self):
        '''random guessing with zero memory space to check if already chosen
        '''
        return random.randint(1,Numbers.gamesize)
    
    def guess4(self):
        '''random guessing with 1 memory space to check last guess if already chosen
        first guess will just return a random guess
        if list 'numbers' is not zero size then it already has guesses in it and
            thus we must thus produce a guess to add to it
        '''
        if len(numbers) == 0:
            return random.randint(1,Numbers.gamesize)  
        else: 
            while True:
                x= random.randint(1,Numbers.gamesize)
                #if guess is not previous value, ie, other player's previous guess, then return x with no further checking
                if x!=numbers[-1] :   
                    return x
    
    def guess5(self):
        '''random guessing with 3 memory locations to check last 3 guesses if already chosen
        first guess will just return a random guess
        if list 'numbers' is not zero size then it already has guesses in it and
            thus we must thus produce a guess to add to it
        '''
        if len(numbers) == 0:
            return random.randint(1,Numbers.gamesize)  
        else: 
            while True:
                x= random.randint(1,Numbers.gamesize)
                #if guess is not in 3 previous values then return x with no further checking
                if x not in numbers[-3:]:
                    return x

    def guess6(self):
        '''guess is simply 1 less than oponent's choice; will check for bounds 
        of guess and uses 1 memory location for strategy [numbers-1] -- last guess; can lose if guess already exists
        first guess will just return a random guess
        '''
        #if no guesses yet, x is random to put into numbers
        if len(numbers) == 0  :
            return random.randint(1,Numbers.gamesize)  
        #if opponent's prev guess was a '1' then return '0' not possible, therefore return random(>=2 of course) (other strategies possible -- eg, max number, etc)
        elif   numbers[-1]==1  :                            
            return random.randint(2,Numbers.gamesize)   
        else:
        #will look at last value guessed by opponent and guess 1 less        
            return numbers[-1] -1                
    
    def guess7(self):
        '''guess is simply 1 less than oponent's choice; will check for bounds 
        of guess and uses 2 memory locations[numbers-1],[numbers-3] opponent's last 2 guesses
        '''
        #if no guesses yet, then return random x
        if len(numbers) == 0:
            return random.randint(1,Numbers.gamesize)
        #[-3] no exists yet if <3, but of course, if >0 then [-1] exists            
        elif len(numbers)<3: 
            #if opponent's prev guess was a '1' then return '0' not possible, therefore return random(>=2 of course) (other strategies possible -- eg, max number, etc)
            if numbers[-1]==1:  
                return random.randint(2,Numbers.gamesize)   
            else: 
           #will look at last value guessed by opponent and guess 1 less            
                return numbers[-1] -1                
        #len >=3 (thus have [-1] and [-3] to use for decisions)        
        elif numbers[-1]==1:                            
        #if opponent's prev guess was a '1' -- lowest possible number, then
            while True:
                x=random.randint(2,Numbers.gamesize)   
                #no return same value as [-1] which is a '1' or as [-3]
                if x!=numbers[-3]:
                        return x
        else:        
        #at this point len>=3 thus [-1],[-3] exist, and [-1] is not '1'
            if numbers[-1]-1 !=numbers[-3]:
                #return 1 less after make sure this value not in [-3]
                return numbers[-1]-1  
            else:
             #[-1]-1 will not work since in [-3] -- need new strategy for guess 
                while True: 
                #various strategies possible, here get random which is not in [-1] or [-3]
                    x=random.randint(1,Numbers.gamesize)
                    if x!=numbers[-1] and x!=numbers[-3]:
                        return x
    
    def guess8(self):
        '''code your own algo here
        currently returns a 1
        '''
        return 1
     
    def guess9(self):
        '''guess is simply 1 more than oponent's choice; will check for bounds 
        of guess and uses 1 memory location for strategy [numbers-1] -- last guess; can lose if guess already exists
        first guess will just return a random guess
        '''
        #if no guesses yet, x is random to put into numbers
        if len(numbers) == 0  :
            return random.randint(1,Numbers.gamesize)  
        #if opponent's prev guess was a max value (ie, gamesize) then return gamesize+1 not possible, therefore return random(<gamesize of course) (other strategies possible -- eg, max number, etc)
        elif   numbers[-1]==Numbers.gamesize  :                            
            return random.randint(1,Numbers.gamesize-1)   
        else:
        #will look at last value guessed by opponent and guess 1 more       
            return numbers[-1] +1                
                  
    def guess10(self):
        '''guess is simply 1 more than oponent's choice; will check for bounds 
        of guess and use 2 memory locations [numbers-1],[numbers-2] last 2 everyone's guesses
        note: in above '1 less' than methods we are using n-1, n-3 memory locations for just
        opponent's guess, but here instead consider opponent's and player's last guesses
        first guess will just return a random guess
        '''
        if len(numbers) == 0:
            return random.randint(1,Numbers.gamesize) 
        #if opponent's prev guess was a max value (ie, gamesize) then return random(<gamesize of course) (other strategies possible -- eg, max number, etc)
        elif   numbers[-1]==Numbers.gamesize  :
            while  True:
                x =  random.randint(1,Numbers.gamesize-1)   
                if x not in  numbers[-2:] :
                    return x
        #will look at last value guessed by opponent and guess 1 more, make sure not in n-2 location
        else:
           if (numbers[-1]+1) not in numbers[-2:]:
                return numbers[-1] +1
           else:
                while True:
                    x=random.randint(1,Numbers.gamesize)
                    if x not in numbers[-2:]:
                           return x            
                  
    def guess11(self):
        '''guess is simply 1 more than oponent's choice; will check for bounds 
        of guess and use 2 memory locations [numbers-1],[numbers-2] last 2 everyone's guesses
        note: in above '1 more use 2 memory locations' were use a different random strategy when
        dealing with next guess for max values or used values
        first guess will just return a random guess
        '''
        if len(numbers) == 0:
            return random.randint(1,Numbers.gamesize)
        #if opponent's prev guess was a max value (ie, gamesize) then return random(<gamesize of course) (other strategies possible -- eg, max number, etc)
        elif   numbers[-1]==Numbers.gamesize  :
            for i in range (1, Numbers.gamesize):
                if i not in numbers[-2:]:
                    return i
        #will look at last value guessed by opponent and guess 1 more, make sure not in n-2 location            
        else:
           if (numbers[-1]+1) not in numbers[-2:]:
                return numbers[-1] +1
           else:
               for i in range (1, Numbers.gamesize):
                    if i not in numbers[-2:]:
                        return i
    
    def guess_text(self,guess_algo):
        '''returns text string describing guess_algo number '''
        guess_list=[\
            'not used at present',
            'random guessing with unlimited space and time constraints',
            'uses mirror strategy -- Alice says x, Bob responds with n+1-x  ',
            'random guessing with zero memory space to check if already chosen []',
            'random guessing with 1 memory space to check last guess if already chosen [n-1]',
            'random guessing with 3 memory locations to check last 3 guesses if already chosen [n-1,2,3]',\
            'guess is simply 1 less than oponent\'s choice; will check for bounds of guess and uses 1 memory location [numbers-1] for strategy -- last guess',
            'guess is simply 1 less than oponent\'s choice; will check for bounds of guess and uses 2 memory locations[numbers-1],[numbers-3] opponent last 2 guesses',
            'code your own algo here (currently just returns a 1)',
            'guess is simply 1 more than oponent\'s choice; will check for bounds of guess and uses 1 memory location [numbers-1] for strategy -- last guess',
            'guess is simply 1 more than oponent\'s choice; will check for bounds of guess and uses 2 memory locations[numbers-1],[numbers-2] opponent\'s last 2 guesses',
            'guess is simply 1 more than oponent\'s choice; check 2 memory locations [numbers-1],[numbers-2] but strategy for guessing when max number exists or previous guesses exist is different']
        if guess_algo >=1 and guess_algo <=11:
            return guess_list[guess_algo]
        else:
            return 'guess algo not specified -- probably random guessing with unlimited space and time constraints'                      
      
    def guess(self,name):
        '''Select the correct guessing algorith for the specified
        player and produce a guess and then try to add it to the list of numbers;
        return if all the numbers have been used up and there is a tie or if a player
        guessed an existing number and loses or if guess simply added to the list of 
        numbers and the game continues'''
        if len(numbers) == Numbers.gamesize:
                if Numbers.no_ties ==0:
                    return 0  #all numbers used up already therefore is a tie game
                else:
                    return -0.1 #added to code later:  use -0.01 as  for loss because all numbers already guessed where ties not allowed
        sg= [\
                self.guess1,
                self.guess1,
                self.guess2,
                self.guess3,
                self.guess4,
                self.guess5,
                self.guess6,
                self.guess7,
                self.guess8,
                self.guess9,
                self.guess10,
                self.guess11]
        if self.guess_algo  <1 or  self.guess_algo >11:
                x= sg[1]()
        else:
                x= sg[self.guess_algo]()  #any guess algo will return some guess x
        y=Numbers.add(x,name) #try to add guess x to 'numbers' -- if returns -1 guess already exists, +1 if valid guess added to numbers
        return y*x   #pos x returned is valid guess, neg x returned indics number exists and player loses 
        
    def print_valid_guess(self,gamesize,x):
        '''After  valid guess want to show guess chosen as well as all the numbers chosen so far,
        as long as the possible list of numbers is not too long'''
        if gamesize < 500:
                   print '{}\'s guess is: {}, all chosen so far: {}'.format(self.name, x,numbers)
        else:
                   print '{}\'s guess is: {}, all chosen so far: {}'.format(self.name, x,'too large to show')
    
    def game_summary(self,name,x,bobalgo,alicealgo):
        '''print statements giving a summary of the game plus calling display_analysis for 
        analysis of the game'''
        print '\nGame Summary:\n-------------'
        if Numbers.gamesize!=0:  
        #early version 0 gamesize was allowed
            if x<0:
                if x==-0.1:  #-0.1 indicates loss because of tie game
                    print  '{} lost because all numbers had already been guessed, and ties (current setting) not allow'.format(name)
                else:
                    print '{} chose {} which already existed, thus {} lost this game.'.format(name,-1*x,name)
            elif x==0:
                print 'Tie Game -- All numbers have been used up.'
            else:
                print 'error: should be tie game or lost game at this point'
        print '\nMaximum turns possible: {}, Turns successfully played: {} ({:0.1f}%)'.format(Numbers.gamesize, len(numbers), (1.0*len(numbers)/Numbers.gamesize)*100  )
        if Numbers.no_ties == 1:
            print "  No ties were allowed (when a player guesses an already chosen number, that player loses, even if no more unchosen numbers exist"
        else:
            print "  Ties were allowed -- if no player has lost and all the numbers have been chosen already, then this is considered a tie"
        print ' Bob\'s algo (Bob moves second) was #{} -- {}\n Alice\'s algo (Alice moves first) was #{} -- {}\n'.format(bobalgo,self.guess_text(bobalgo),alicealgo,self.guess_text(alicealgo))
        if Numbers.bp.bob!= 0:
                    print 'Batch parameters : {}'.format(Numbers.bp)        
        Numbers.display_analysis()
             
        
def main():
    Numbers.welcome()
    while True:
        #set up parameters for game and for Bob and Alice
        if Numbers.bp.bob== 0: 
            Numbers.choose_gamesize()            
        else:  
            Numbers.gamesize=Numbers.bp.n
        Alice = Player('Alice',Numbers.bp)
        Bob = Player('Bob',Numbers.bp)
        start_time= time.clock() 
        
        if  Numbers.bp.times==0 :
            print "Running a single game.... let's start....\n-----------------------------------------"
            #Alice, first move, and then Bob take guesses
            while True:
                
                x=Alice.guess(Alice.name)
                if x <= 0:  
                #-1 lost game, 0 tie game, +1 valid guess and continue game
                    Alice.game_summary(Alice.name,x,Bob.guess_algo,Alice.guess_algo)
                    break
                else:  
                    Alice.print_valid_guess(Numbers.gamesize,x)             
               
                x=Bob.guess(Bob.name)
                if x <=0:   
                    Bob.game_summary(Bob.name,x,Bob.guess_algo,Alice.guess_algo)
                    break
                else:  
                    Bob.print_valid_guess(Numbers.gamesize,x)             
          
        else:   
        #run as multiple 'times' game run
            for i in range(Numbers.bp.times):
                print  "Batch run of {} games -- running game {}\n---------------------------------------------------".format(Numbers.bp.times, i+1)
                del numbers[:] 
                while True:
                   
                  x=Alice.guess(Alice.name)
                  if x <=0:   
                        Alice.game_summary(Alice.name,x,Bob.guess_algo,Alice.guess_algo)
                        if x<0:
                            Numbers.batch_array.append(1)  
                            #-1 Bob lost and Alice won, +1 Alice lost and Bob won
                        else:
                            Numbers.batch_array.append(0)   
                            #0 means tie game
                        break
                  else:  
                        Alice.print_valid_guess(Numbers.gamesize,x)                  

                  x=Bob.guess(Bob.name)
                  if x <=0:  
                        #-1 lost game, 0 tie game
                        Bob.game_summary(Bob.name,x,Bob.guess_algo,Alice.guess_algo)
                        if x<0:
                            Numbers.batch_array.append(-1)  
                            #-1 Bob lost and Alice won, +1 Alice lost
                        else:
                            Numbers.batch_array.append(0)   
                            #0 means tie game
                        break
                  else:  
                         Bob.print_valid_guess(Numbers.gamesize,x)
      
           #out of for multiple game for loop now, and now print out a batch summary of the multiple games just run
            Numbers.batch_game_summary(Bob.guess_text(Bob.guess_algo),Alice.guess_text(Alice.guess_algo))  
               
        #at this point: break from single game while loop or finished code (batch summary) of the multiple game 'else' block
        end_time=time.clock()
        Numbers.time_complexity_analysis(start_time,end_time)
        #run new game or exit?
        Numbers.erase() 
        try: 
            aa=raw_input("Do you want to play again? [y/n] or [b, batch, 1,2{,3,4}]: \a")
            if aa in ['batch','b','version','g'] or aa[0] in ['0','1','2','3','4','5','6','7','8','9']:
                Numbers.bp=Numbers.Batchy._make(Numbers.batch_input(aa))
            else:
                if aa in ['','y','yes','Yes','YES','yup','ok','sure']:
                    continue 
                    #run next game as non-batch input of parms since erase has reset to [0,0,0,0]
                else:
                    print "I have interpreted your input as not to replay the game.\nThank you for playing with me. Game over."
                    break 
                    #break out of main() while loop
        except:
            continue
            #continue main() while loop, thus new single/batch game will occur
      

if __name__=="__main__":
    print '\n\n------------------START PROGRAM----------------\n\n'
    main()
    print '\n\n----------------STOP (END) PROGRAM--------------\n\n'

    