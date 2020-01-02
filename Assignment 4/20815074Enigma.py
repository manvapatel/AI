from prison import Player
from collections import Counter
class Enigma(Player):

    def studentID(self):
        """ Returns the creator's numeric studentID """
        return "20815074"
        #raise NotImplementedError("studentID not implemented")

    def agentName(self):
        """ Returns a creative name for the agent """
       	return self.__class__.__name__

    def play(self, myHistory, oppHistory1, oppHistory2):
        """ 
        Given a history of play, computes and returns your next move
        ( 0 = cooperate; 1 = defect )
        myHistory = list of int representing your past plays
        oppHisotry1 = list of int representing opponent 1's past plays
        oppHisotry2 = list of int representing opponent 2's past plays
        NB: use len(myHistory) to find the number of games played
        """
        len_history = len(myHistory)
        
        #in the beginning of the match, when there will be no history, the agent cooperates
        if(len_history==0):
            return 0
                    
        if(len_history>=1):

            #Counter returns the number of times a particular value occurs in a list
            data_player1 = Counter(oppHistory1)
            data_player2 = Counter(oppHistory2)

            #If the number of times the player has cooperated is equal to the number of times it has defected, 
            #then the agent predicts that the player will defect in the next move as well. Otherwise, it predicts the
            #outcome which has occured the most in the history.  
            if(data_player1['0']==data_player1['1']):
                previous_move_player1 = 1
            else:
                previous_move_player1 = data_player1.most_common(1)[0][0]

            if(data_player2['0']==data_player2['1']):
                previous_move_player2 = 1
            else:
                previous_move_player2 = data_player2.most_common(1)[0][0]
            
            
            #If both the players tend to cooperate, then agent cooperates. Otherwise it defects.
            if(previous_move_player1 == 0 and previous_move_player2 == 0):
                return 0
            elif(previous_move_player1 == 1 and previous_move_player2 == 0):
                return 1
            elif(previous_move_player1 == 0 and previous_move_player2 == 1):
                return 1
            elif(previous_move_player1 == 1 and previous_move_player2 == 1):
                return 1
