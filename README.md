
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
        player has lost yet.


The space complexity of mirror games

Sumegha Garg, Jon Schneider
(Submitted on 8 Oct 2017)
We consider a simple streaming game between two players Alice and Bob, which we call the mirror game. In this game, Alice and Bob take turns saying numbers belonging to the set {1,2,…,2N}. A player loses if they repeat a number that has already been said. Bob, who goes second, has a very simple (and memoryless) strategy to avoid losing: whenever Alice says x, respond with 2N+1−x. The question is: does Alice have a similarly simple strategy to win that avoids remembering all the numbers said by Bob? 
The answer is no. We prove a linear lower bound on the space complexity of any deterministic winning strategy of Alice. Interestingly, this follows as a consequence of the Eventown-Oddtown theorem from extremal combinatorics. We additionally demonstrate a randomized strategy for Alice that wins with high probability that requires only O~(N−−√) space (provided that Alice has access to a random matching on K2N). 
We also investigate lower bounds for a generalized mirror game where Alice and Bob alternate saying 1 number and b numbers each turn (respectively). When 1+b is a prime, our linear lower bounds continue to hold, but when 1+b is composite, we show that the existence of a o(N) space strategy for Bob implies the existence of exponential-sized matching vector families over ZN1+b.
Comments:	13 pages
Subjects:	Computational Complexity (cs.CC); Discrete Mathematics (cs.DM)
Cite as:	arXiv:1710.02898 [cs.CC]
