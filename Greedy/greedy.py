from itertools import product
#ASSIGNMENT CLASS IS JUST FOR INITIALISATION WHILE GENERATING THE ASSIGNMENT
class Assignment :

    def __init__(self, time_interval = "", event = "", score = 0, location = None, valid = True, update = True):
        
        self.time_interval = time_interval
        self.event = event
        self.score = score
        self.location = location
        self.valid = valid
        self.update = update

class GRE:
    def __init__(self,U = [],E = [],T = [],location = [],sigma = [],mu_E = [],mu_C = []):
        self.U = U[:]
        self.S = []
        self.A = []
        self.E = E[:]
        self.T = T[:]
        self.location = location

        self.sigma = sigma
        self.mu_E = mu_E
        self.mu_C = mu_C


    #EQUATION 2 OF THE PAPER SMALL OMEGA(w)-> EXPECTED ATTENDANCE FOR AN EVENT E SCHEDULED TO TAKE PLACE AT T
    def score(self,event, time_interval, S) :

        net_score = 0

        for u in range(len(self.U)) :

                summation_of_rho = self.prob_e_t_u(event, time_interval, u, S)

                net_score += summation_of_rho

        return net_score


    # calculating rho -> probability of 'U' attending 'E' at 'T'
    def prob_e_t_u(self,e, time_interval, u, S) :

        #INTEREST OF USER U OVER EVENT E
        mu_u_e = self.mu_E[u][e]
        #PROBABILITY OF USER U PARTICIPATING IN A SOCIAL ACTIVITY AT TIME T
        sigma_u_t = self.sigma[u][time_interval]

        mu_u_c = 0
        #calculating summation of mu_u_c ->SUMMATION OF INTEREST OF USER U OVER THE COMPETING EVENT
        for c in range(len(self.mu_C[u])) :

                if c == time_interval :
                        mu_u_c += self.mu_C[u][c]

        mu_u_p = 0
        #calculating summation of mu_u_p->SUMMATION OF INTEREST OF USER U OVER EVENTS IN THE SCHEDULE 
        for p in S :
            if p.time_interval == time_interval :
                    mu_u_p += self.mu_E[u][p.event]
                    #print("mu_u_p",mu_u_p)
        rho = sigma_u_t * (mu_u_e / (mu_u_c + mu_u_p))
        return rho

    #EQUATION 4 IN THE PAPER
    #NEW SCORE IS ALSO REFERRED TO AS THE GAIN IN EXPECTED ATTENDANCE BY INCLUDING THE ASSIGNMENT IN THE SCHEDULE S
    def update_score(self,assignment,best_assignment) :

        new_score = 0 
        old_score = 0

        new_S = self.S + [assignment]

        for i in new_S :
                new_score += self.score(i.event, assignment.time_interval, new_S)

        for i in self.S :
                old_score += self.score(i.event, assignment.time_interval, self.S)

        #assignment.score = score(assignment.event,assignment.time_interval, S+[assignment]) - score(assignment.event, assignment.time_interval, S)
        assignment.score = new_score - old_score
        return assignment.score


    def update_assignment(self,A, best_assignment):
        print("\n")
        print("Assignments to be updated")
        print("\n")
        
        for i in A :

                if i.time_interval == best_assignment.time_interval and i.valid :
                        print('( ', i.time_interval+1, ' a ', i.event+1, ')')
                        i.score = self.update_score(i,best_assignment)
        print("\n")

  

    def remove_assignment(self,A,best_assignment): 
            
        best_assignment.valid=False  #REMOVING BEST ASSIGNMENT FROM THE ASSIGNMENT SET
        for assignment in A:
            #IF LOCATION AND TIME INTERVAL CLASH OR IF THEY ARE THE SAME EVENTS THEN SET THEIR VALIDITY TO BE FALSE
            if ((assignment.location==best_assignment.location and assignment.time_interval==best_assignment.time_interval) or (assignment.event==best_assignment.event)):
                    assignment.valid=False




    def generate_assigment(self,events,time_intervals):
        #GENERATES AN ASSIGNMENT BETWEEN EVENTS AND TIME INTERVALS AND LOCATIONS 

        #GENERATING CROSS PRODUCT BETWEEN EVENTS AND TIME INTERVALS
        c=list(product(events,time_intervals))
        #print(c)
        for i in c :
            a = Assignment(i[1],i[0],location= self.location[i[0]])
            self.A.append(a)


    def greedy_alg(self,k=3):


        self.generate_assigment(list(range(len(self.E))),list(range(len(self.T))))
        self.assign_score()
        self.display()
        final_selection_list=[0 for i in range(k)]
        for i in range(k):
            best_assignment=self.select_assignment()
            print("Selection:", self.E[best_assignment.event],' ', self.T[best_assignment.time_interval], ' ', best_assignment.score)
            final_selection_list[i]=[self.E[best_assignment.event],self.T[best_assignment.time_interval]]
            self.S.append(best_assignment)
            self.remove_assignment(self.A,best_assignment)
            self.update_assignment(self.A,best_assignment)
            self.display()
        # for i in self.S:
        #     print(i.time_interval,i.event)
        print("FINAL SELECTION LIST : ",final_selection_list)




    #SELECTING THE ASSIGNMENT WITH THE HIGHEST SCORE
    def select_assignment(self):

        max_assignment = Assignment()
        max_assignment.score = float('-inf')

        for i in self.A :

                if (i.score > max_assignment.score) and i.valid :
                        max_assignment = i


        return max_assignment


    def assign_score(self) :

        for i in self.A :
                i.score = self.score(i.event, i.time_interval, self.S+[i])



    #------------------------------------------------------------------------------------------------------------

    def display(self,assignment_list = None) :
        if assignment_list == None :
                assignment_list = self.A
        print("\n")
        print("\n")
        print("-------------------------------------------------------------")
        print("Event  Time Interval  Score  Location  Validity")
        for i in assignment_list :
            print(self.E[i.event], '   ', self.T[i.time_interval], '           ', '{:.5}'.format(str(i.score)), '', '{:7}'.format(i.location), ' ', i.valid)
        print("--------------------------------------------------------------")
        print("\n")
        print("\n")

if __name__ == '__main__':
    # users=[]
    # n=int(input("Enter number of users : "))
    # i=1
    # while(n):
    #         print("Enter user #",i)
    #         a=input()
    #         i+=1
    #         users.append(a)
    #         n-=1

    # candidate=[]
    # n=int(input("Enter number of candidate events : "))
    # i=1
    # while(n):
    #         print("Enter candidate event #",i," : ")
    #         a=input()
    #         i+=1
    #         candidate.append(a)
    #         n-=1

    # location=[]
    # n=len(candidate)
    # for i in range(n):
    #         print("Enter location for candidate event ",candidate[i])
    #         a=input()
    #         location.append(a)

    # time=['t1','t2']
    # active_prob=[[0 for i in range(len(time))] for i in range(len(users))]
    # for i in range(len(users)):
    #         for j in range(len(time)):
    #                 print("Enter social activity probability of",users[i],"at time",time[j]," : ")
    #                 a=float(input())
    #                 active_prob[i][j]=a

    # event_interest=[[0 for i in range(len(candidate))] for i in range(len(users))]
    # for i in range(len(users)):
    #         for j in range(len(candidate)):
    #                 print("Enter event interest of",users[i],"of candidate event",candidate[j]," : ")
    #                 a=float(input())
    #                 event_interest[i][j]=a

    # competing_events=['c1','c2']
    # competing_event_interest=[[0 for i in range(len(competing_events))] for i in range(len(users))]
    # for i in range(len(users)):
    #         for j in range(len(competing_events)):
    #                 print("Enter competing event interest of",users[i],"of the competing event",competing_events[j]," : ")
    #                 a=float(input())
    #                 competing_event_interest[i][j]=a
    #I HAVE FIXED 2 TIME INTERVALS T1 AND T2 AND 2 COMPETING EVENTS C1 AND C2 AS IN THE PAPER 
    # test=GRE(users,candidate,time,location,active_prob,event_interest,competing_event_interest)
    test=GRE(['u1','u2'],['e1','e2','e3','e4'],['t1','t2'],['Stage 1', 'Stage 1', 'Stage 2', 'Room A'],[[0.8, 0.5],[0.5, 0.7]],[[0.9, 0.3, 0, 0.6],[0.2, 0.6, 0.1, 0.6]],[[0.8, 0.3],[0.4, 0.7]])
    test.greedy_alg()