from itertools import product
import sys
from operator import attrgetter
from imports import SES
sys.path.insert(0, '../imports')
from itertools import product
from operator import attrgetter
import time
print("Which Algorithm do you wanna look into")
print("1)GREEDY ALGORITHM")
print("2)Incremental Updating scheme")
print("3)Horizontal Assignment Algorithm")
print("4)Horizontal Assignment with Incremental Updating")
n=int(input("Enter your preferred choice : "))
if(n==1):
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
		start = time.time()
		test=GRE(['u1','u2'],['e1','e2','e3','e4'],['t1','t2'],['Stage 1', 'Stage 1', 'Stage 2', 'Room A'],[[0.8, 0.5],[0.5, 0.7]],[[0.9, 0.3, 0, 0.6],[0.2, 0.6, 0.1, 0.6]],[[0.8, 0.3],[0.4, 0.7]])
		test.greedy_alg()
		end=time.time()
		#print("Runtime of the Greedy Program is",end - start)

if(n==2):
	class List_timeInt :

		def __init__(self, time_interval = None, l = [], update = True):
			
			self.time_interval = time_interval
			self.l = l[:]
			self.update = update

	class Assignment :

	        def __init__(self, time_interval = "", event = "", score = 0, location = None, valid = True, update = True):
	                
	                self.time_interval = time_interval
	                self.event = event
	                self.score = score
	                self.location = location
	                self.valid = valid
	                self.update = update
	class INC:

		def __init__(self,k = 0, U = [], E = [], T = [], location = [] ,social_active_probabilities = [],event_attendance_probability = [] ,competing_event_attendance_probability = []):
			
			self.k = k
			self.U = U
			self.E = E
			self.T = T
			self.location = location

			self.sigma = social_active_probabilities
			self.mu_E = event_attendance_probability
			self.mu_C = competing_event_attendance_probability


			self.A = []
			self.S = []

			self.L_i = [List_timeInt(i) for i in self.T]
			self.M = [Assignment() for i in self.T]
			self.bound = Assignment()

		#-------------------GENERATE ASSIGNMENT LIST-------------------------------
		
		def generate_assignment(self,events,time_intervals) : 

			events = list(range(len(self.E)))
			time_intervals = list(range(len(self.T)))


			c=list(product(events,time_intervals))



			for i in c :

				t_a_e = Assignment(i[1],i[0], location= self.location[i[0]])
				self.A.append(t_a_e)

				self.L_i[t_a_e.time_interval].l.append(t_a_e)



			self.assign_score()


		def getBetterAssignment(self, current_assignment, t_a_e) :

			if t_a_e.score > current_assignment.score :
		
				current_assignment = t_a_e

			return current_assignment


		def assign_score(self) :

			for i in self.A :
				i.score = self.score(i.event, i.time_interval, self.S+[i])
				self.M[i.time_interval] = self.getBetterAssignment(self.M[i.time_interval],i)




		#-------------------SCORE CALCULATION------------------
		
		def score(self, event, time_interval, S) :
			net_score = 0

			for u in range(len(self.U)) :

				p = self.prob_e_t_u(event, time_interval, u, S)

				net_score += p

			return net_score

		def prob_e_t_u(self, event, time_interval, u, S) :

			mu_u_e = self.mu_E[u][event]

			sigma_u_t = self.sigma[u][time_interval]

			mu_u_c = 0
			for c in range(len(self.mu_C[u])) :

				if c == time_interval :
					mu_u_c += self.mu_C[u][c]

			mu_u_p = 0
			for p in S :

				if p.time_interval == time_interval :
					mu_u_p += self.mu_E[u][p.event]

			p = sigma_u_t * (mu_u_e / (mu_u_c + mu_u_p))

			return p

		def update_score(self,assignment,best_assignment) :

			new_score = 0 
			old_score = 0

			new_S = self.S + [assignment]

			for i in new_S :
				new_score += self.score(i.event, assignment.time_interval, new_S)

			for i in self.S :
				old_score += self.score(i.event, assignment.time_interval, self.S)

			assignment.score = new_score - old_score
			return assignment.score


		#-------------------------UPDATE LIST INTERVAL-----------------------------------

		def update__L_i(self, top_assignment) : # line 9-10 
			self.L_i[top_assignment.time_interval].l.remove(top_assignment)
			top_assignment.U=False
			self.L_i[top_assignment.time_interval].update=False

			for event in self.L_i[top_assignment.time_interval].l:
				event.update=False


		#-------------------------UPDATE TOP VALID UPDATED ASSIGN LIST -------------------

		def update_M(self, top_assignment) : # line 11-15
			for i in range(len(self.M)):
				if (self.M[i].time_interval==top_assignment.time_interval):
					self.M[i].score=float("-inf")
					self.M[i].valid=False
				elif (self.M[i].event==top_assignment.event):
					#self.status_log(self.L_i[i].l)
					self.M[i]=self.get_top_assignment(self.L_i[i].l)


		#-------------------------FIND BOUND(Φ)-------------------
		def get_bound(self) : # line 16

			flag = False

			for i in self.M :
				if i.update and i.valid :
					flag = True

			top_scorer = Assignment(score = "unavailable")
			if flag :
				top_scorer=max(self.M, key=attrgetter('score'))

			return top_scorer


		#------------------------UPDATE ASSIGNMENTS-----------------------------

		def update_assignments(self,top_assignment):

			update_assignment_list = []
			for i in range(len(self.T)):

				if self.bound.score == "unavailable" :
					max = Assignment()
					for j in range(len(self.A)) :
						if self.A[j].valid and self.A[j].score > max.score :
							max = self.A[j]

					self.update_score(max,top_assignment)
					max.update = True
					update_assignment_list.append(max)
					self.bound = max

					break


				if self.L_i[i].update==False and self.M[i].score<=self.bound.score:

					j = 0
					while j < len(self.L_i[i].l) :

						#
						if self.L_i[i].l[j].valid==False:
							self.L_i[i].l.pop(j)


						elif self.L_i[i].l[j].update==False and self.L_i[i].l[j].score >=self.bound.score:
							self.update_score(self.L_i[i].l[j],top_assignment)
							self.L_i[i].l[j].update=True
							update_assignment_list.append(self.L_i[i].l[j])
							self.M[i] = self.getBetterAssignment(self.M[i],self.L_i[i].l[j])

							self.bound = self.getBetterAssignment(self.bound,self.L_i[i].l[j])

						j += 1

						
					temp=0
					for j in self.L_i[i].l:
						if j.update==False:
							temp=1
							break
					if temp==0:
						self.L_i[i].update=True
					


			for i in range(len(self.M)):
				
				print("M[i] = ", self.printer_assignment(self.M[i]))


				for j in range(len(self.L_i[i].l)):


					print("L_i.l= ",self.printer_assignment(self.L_i[i].l[j]))
					if self.L_i[i].l[j].valid == True and self.L_i[i].l[j].update == True :

						self.M[i] = self.getBetterAssignment(self.M[i],self.L_i[i].l[j])

						
			self.printer_updated_assignments(update_assignment_list)


	
		#-------------------------SELECT TOP VALID UPDATED ASSIGNMENT-------------

		def get_top_assignment(self,array=None):
			max_assignment = Assignment()
			max_assignment.score = float('-inf')

			if array == None:
				array=self.A
			
			for i in array:
				if (i.score > max_assignment.score) and (i.valid==True) and (i.update == True):
					max_assignment = i



			return max_assignment

		def update_validity(self,top_assignment) :

			for assignment in self.A:
				if ((assignment.location==top_assignment.location and assignment.time_interval==top_assignment.time_interval) or (assignment.event==top_assignment.event)):
					assignment.valid=False
		

		#----------------------INC ALGORITHM------------------------------
		def INC_algo(self,k=3) :
			self.generate_assignment(list(range(len(self.E))),list(range(len(self.T))))

			self.assign_score()
			final_selection_list=[0 for i in range(k)]

			self.display(self.A)
			final_selection_list=[0 for i in range(k)]
			for i in range(k) :	
				top_assignment = self.get_top_assignment(self.M)
				
				print("top_assignment: ",self.E[top_assignment.event], self.T[top_assignment.time_interval])
				final_selection_list[i]=[self.E[top_assignment.event], self.T[top_assignment.time_interval]]
				self.update_validity(top_assignment)
				

				self.S.append(top_assignment)

				self.update__L_i(top_assignment)
				

				self.update_M(top_assignment)
				
				self.bound = self.get_bound()

				print("                       DISPLAY 1                         ")
				self.display(self.A)
				

				

				self.update_assignments(top_assignment)
				
				print("                       DISPLAY 2                         ")
				self.display(self.A)

			print("FINAL SELECTION LIST : ",final_selection_list)

		#----------------------------------------------------------------

		#--------------------------------------------------------DISPLAY----------------------------------------------
		def display(self,assignment_list) :

			print("\n")
			print("\n")
			print("-------------------------------------------------------------")
			print("Event  Time Interval  Score  Location  Validity")

			for i in assignment_list :
				print(self.E[i.event], '   ', self.T[i.time_interval], '           ', '{:.5}'.format(str(i.score)), '', '{:7}'.format(i.location), ' ', i.valid)

			print("--------------------------------------------------------------")
			print("\n")
			print("\n")

		def printer_assignment(self,assignment):

			if assignment.event == '' :
				return str(assignment.time_interval + "_a_" + assignment.event)
				
			return str(self.T[assignment.time_interval] + "_a_" + self.E[assignment.event])


		def printer_updated_assignments(self,UA_list):

			print("Updated Assignments:  ",end = ' ')

			for j in UA_list :
				if j.update :
					print(self.printer_assignment(j),end = "  ")

			print("\n\n")
			
	if __name__ == '__main__':
		start=time.time()
		S=[]
		U=['u1','u2']
		A=[]
		E=['e1','e2','e3','e4']
		T=['t1','t2']
		location=['Stage 1', 'Stage 1', 'Stage 2', 'Room A']
		sigma=[[0.8, 0.5],[0.5, 0.7]]
		mu_E=[[0.9, 0.3, 0, 0.6],[0.2, 0.6, 0.1, 0.6]]
		mu_C=[[0.8, 0.3],[0.4, 0.7]]
		test = INC(3, U, E , T , location ,sigma,mu_E,mu_C)
		test.INC_algo()
		end=time.time()
		#print("Runtime of the Incremental Updating Scheme is",end - start)
if(n==3):
	class Assignment :

		def __init__(self, time_interval = "", event = "", score = 0, location = None, valid = True, update = True):
			
			self.time_interval = time_interval
			self.event = event
			self.score = score
			self.location = location
			self.valid = valid
			self.update = update

	class HOR(SES):

		def __init__(self,k = 0, U = [], E = [], T = [], location = [] ,social_active_probabilities = [],event_attendance_probability = [] ,competing_event_attendance_probability = [],verbose=True):
			
			super().__init__(k , U , E , T , location  ,social_active_probabilities ,event_attendance_probability ,competing_event_attendance_probability )

			self.L_i = [[] for i in self.T]
			self.verbose=verbose


		#-------------------------------GENERATE ASSIGNEMENT LIST------------------------------
		def getAssign(self,e,time):
			for i in self.A:
				if i.event == e and i.time_interval == time:
					return i


		def generate_assignment(self):

			super().generate_assignment()

	    	#list for all available events
			se= set(list(map(lambda x: x.event, self.S))) #List for all events in the schedule set

			e = set(list(range(len(self.E))))

			diff_e = e.difference(se)


			events = list(diff_e) 


			time_intervals = list(range(len(self.T)))  #list of time intervals
			c = list(product(events,time_intervals))   #All possible combinations of events and time intervals


			for i in c:
				x=self.getAssign(i[0],i[1])   #returns assignment with the given event and time interval
				self.print_assignment(x)
				if x.valid == True:
					x.score = self.score(x.event, x.time_interval, self.S+[x])
					self.L_i[i[1]].append(x)
					if self.M[i[1]].event == "":
						self.M[i[1]] = x
					self.M[i[1]] = self.getBetterAssignment(self.M[i[1]],x)

			

		#--------------------------------------------------------------------------------------


		def popTopAssgn(self) : 
			top=None
			index=None
			for i in range(len(self.M)):
				if(self.M[i].event  == ""):
					continue
				elif((top == None) or (top.score < self.M[i].score)):
					top=self.M[i]
					index=i

			if index != None :
				self.M[index] = Assignment()

			return top

		#----------------------------SELECT and UPDATE ASSIGNMENT from M----------------------------------

		def select_update_assgn(self) :
			for i in range(len(self.M)):

				self.status_log(self.S,verbose=self.verbose)

				if(len(self.S) >= self.k):
					break

				ass=self.popTopAssgn()

				eve=[i.event for i in self.S]
				eve=list(filter(lambda z : z!=None,eve))

				if len(eve)!=0 and ass.event in eve:
					has=True
				else:
					has=False

				if(has == False):

					self.S.append(ass)
				else:
					tp=None
					for i in self.L_i[ass.time_interval]:
						if((tp == None or tp.score < i.score) and self.not_belongs_to_S(i)): #new function needed for param
							tp=i

					
					self.M[tp.time_interval]=tp 
						    
		def not_belongs_to_S(self,param):  #returns true if param doesnt belong to S
			for i in range(len(self.S)):
				if(self.S[i].event == param.event):
					return False
			return True

		def status_log(self,assignment_list = None,verbose=True) :
			if verbose==True:
				if assignment_list == None :
					assignment_list = self.A

				print()
				print()
				print("-------------------------------------------------------------")

				print("Event  Time Interval  Score  Location  Validity")

				for i in assignment_list :

					if len(str(i.score)) >= 5 :

						print(self.E[i.event], '   ', self.T[i.time_interval], '           ', '{:.5}'.format(str(i.score)), '', '{:7}'.format(i.location), ' ', i.valid)

					else :
						print(self.E[i.event], '   ', self.T[i.time_interval], '           ', '{:5}'.format(str(i.score)), '', '{:7}'.format(i.location), ' ', i.valid)

				self.print_M()
				print("--------------------------------------------------------------")
				print()
				print()

		def hor_algorithm(self) :

			while(len(self.S)<self.k):

				self.status_log(verbose=self.verbose)

				self.generate_assignment()

				self.select_update_assgn()
	if __name__ == '__main__':
		start=time.time()
		K=3
		U = ['u1','u2']
		S = []
		A = []
		E = ['e1','e2','e3','e4']
		T = ['t1','t2']
		location = ['Stage 1', 'Stage 1', 'Stage 2', 'Room A']

		sigma = [[0.8, 0.5],[0.5, 0.7]]
		mu_E = [[0.9, 0.3, 0, 0.6],[0.2, 0.6, 0.1, 0.6]]
		mu_C = [[0.8, 0.3],[0.4, 0.7]]

		hor_object = HOR(K, U, E , T , location ,sigma,mu_E,mu_C)
		hor_object.hor_algorithm()
		hor_object.status_log()
		hor_object.status_log(hor_object.S)
		end=time.time()
		#print("Runtime of the Horizontal Assignment Algorithm is ",end - start)

if(n==4):
	start=time.time()
	sys.path.insert(0,'../HOR')
	from hor import HOR
	class Assignment :
		def __init__(self, time_interval = "", event = "", score = 0, location = None, valid = True, update = True):
		    
		    self.time_interval = time_interval
		    self.event = event
		    self.score = score
		    self.location = location
		    self.valid = valid
		    self.update = update
	class List_timeInt :
		def __init__(self, time_interval = None, l = [], update = True):
			
			self.time_interval = time_interval
			self.l = l[:]
			self.update = update
	class HOR_I(HOR) :

		def __init__(self,k = 0, U = [], E = [], T = [], location = [] ,social_active_probabilities = [],event_attendance_probability = [] ,competing_event_attendance_probability = [],verbose=True):
			
			super().__init__(k , U , E , T , location  ,social_active_probabilities ,event_attendance_probability ,competing_event_attendance_probability )
			self.verbose=verbose

		def hor_i__algo(self) :

			while(len(self.S) < self.k) :

				if self.S == [] :
					self.generate_assignment() 

				else :

					for i in range(len(self.T)) :
						self.inc_assgnmnt_update(i) 


				if self.select_update_assgn() == None :
					return self.S
			return self.S
		end=time.time()
		#print("Runtime of the Horizontal Assignment with Incremental Updating ",end - start)




		#---------------------------INCREMENTAL ASSIGNMENTS UPDATING-----------------------------------------

		def inc_assgnmnt_update(self, time_interval, top_assignment=None) : 
			self.bound.score=0  
			j=0
			while j < len(self.L_i[time_interval]): 
				if self.L_i[time_interval][j].valid==True:
					if self.L_i[time_interval][j].score >= self.bound.score:
						self.update_score(self.L_i[time_interval][j],top_assignment)
						self.L_i[time_interval][j].update == True
						self.bound = self.getBetterAssignment(self.bound,self.L_i[time_interval][j])
					else:
						self.L_i[time_interval][j].update == False
				else:
					self.L_i[time_interval].pop(j)
				j=j+1
			self.M[time_interval]=self.bound


		def select_update_assgn(self): 
			for i in range(len(self.M)):

				self.status_log(self.S,verbose=self.verbose)

				if(len(self.S) >= self.k):
					break

				ass=self.popTopAssgn()

				if ass == None :
					return None

				eve=[i.event for i in self.S]
				eve=list(filter(lambda z : z!=None,eve))

				if len(eve)!=0 and ass.event in eve:
					has=True
				else:
					has=False

				if(has is False):

					self.S.append(ass)

				else:
					tp=None
					for i in self.L_i[ass.time_interval]:
						if((tp == None or tp.score < i.score) and i.update == True and self.not_belongs_to_S(i)): 
							tp=i
					self.M[tp.time_interval]=tp

					if(tp== None and self.valid(ass)):
						self.inc_assgnmnt_update(tp.time_interval)
			
			return 1
			




		
