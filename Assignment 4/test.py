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
        
        if(len_history==0):
            return 0
                    
        if(len_history>=1):
            data_player1 = Counter(oppHistory1)
            data_player2 = Counter(oppHistory2)
            if(data_player1['0']==data_player1['1']):
                previous_move_player1 = 1
            else:
                previous_move_player1 = data_player1.most_common(1)[0][0]

            if(data_player2['0']==data_player2['1']):
                previous_move_player2 = 1
            else:
                previous_move_player2 = data_player2.most_common(1)[0][0]
            
            #previous_move_player1 = oppHistory1[len_history-1]
            #previous_move_player2 = oppHistory2[len_history-1]

            if(previous_move_player1 == 0 and previous_move_player2 == 0):
                return 0
            elif(previous_move_player1 == 1 and previous_move_player2 == 0):
                return 1
            elif(previous_move_player1 == 0 and previous_move_player2 == 1):
                return 1
            elif(previous_move_player1 == 1 and previous_move_player2 == 1):
                return 1
