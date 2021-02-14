######################################
# The KB class will store information about your interactions with the game.  
# You will use the KB to help you make a decision about where to move next.  
# So, for example, if you use the MOVE command and the game gives you the following results:  

# You are in room 4.
# Passages lead to [1, 3, 8]
# I smell a Wumpus!
#
# The KB would suggest which is a better option of the three possibilities using previous facts and inference.
#####################################
import aima3.utils
import aima3.logic

class KB():

    
    clauses = []
    breeze=[]
    not_breeze=[]
    smell=[]
    not_smell=[]
    safe=[]
    conns={}

    def __init__(self):
        self.conns["1"] = [2,4,5]
        self.conns["2"] = [3,1,6]
        self.conns["3"] = [4,2,7]
        self.conns["4"] = [1,3,8]
        self.conns["5"] = [1,6,8]
        self.conns["6"] = [2,7,5]
        self.conns["7"] = [3,8,6]
        self.conns["8"] = [4,5,7]



    def smell_info(self, location, smell_wumpus):
        if smell_wumpus:
            if str(location) not in (self.smell):
                self.smell.append(str(location))
        else:
            if str(location) not in (self.not_smell):
                self.not_smell.append(str(location))


    def breeze_info(self, location, feel_breeze):
        if feel_breeze:
            if str(location) not in (self.breeze):
                self.breeze.append(str(location))
        else:
            if str(location) not in (self.not_breeze):
                self.not_breeze.append(str(location))

    def location_info(self, current_room):
        suggestion=""
        if not str(current_room) in self.safe:
            self.safe.append(str(current_room))

    def make_suggestion(self, options):
        suggestion=""
        for rm in options:
            found=False
            if str(rm) in self.smell and str(rm) in self.breeze:
                if str(rm) in self.safe:
                    suggestion =suggestion + "You have been here before but you could safely move to room "  + str(rm) + "\n"
                    found=True
                else:
                    suggestion =suggestion + "Strong suggestion to move to room "  + str(rm) + "\n"
                    found=True
            else:
                #print("Step 1")
                if not rm in self.breeze:
                    #print("Step 2")
                    conns_to_room=self.conns[str(rm)]
                    #print("is " + str(conns_to_room) + " in " + str(self.breeze))
                    counter=0
                    for rm_conn in conns_to_room:
                        if rm_conn==rm:
                            continue
                        ##If one of the connected rooms senses a breeze then maybe the room has a pit
                        if str(rm_conn) in self.breeze:
                            counter = counter + 1

                    if counter ==1  and str(rm) not in self.safe:
                        suggestion =suggestion + "Uh oh: There is a chance that room " + str(rm) + " could mean trouble.\n" 
                        found=True
                    elif counter >=2  and str(rm) not in self.safe:
                        suggestion =suggestion + "Uh oh: Room " + str(rm) + " means trouble.\n"
                        found=True

                if not rm in self.smell:
                    #print("Step 3")
                    conns_to_room=self.conns[str(rm)]
                    #print("is " + str(conns_to_room) + " in " + str(self.smell))
                    counter=0
                    for rm_conn in conns_to_room:
                        if rm_conn==rm:
                            continue
                        ##If one of the connected rooms senses a smell then maybe the room has a wumpus
                        if str(rm_conn) in self.breeze:
                            counter = counter + 1
                    if counter ==1  and str(rm) not in self.safe:
                        suggestion =suggestion + "Uh oh: There is a chance that room " + str(rm) + " could mean trouble.\n" 
                        found=True
                    elif counter >=2  and str(rm) not in self.safe:
                        suggestion =suggestion + "Uh oh: Room " + str(rm) + " means trouble.\n"
                        found=True

            if not found:
                if str(rm) in self.safe:
                    suggestion =suggestion + "Sometimes safety is a place you've been before, try room "  + str(rm) + "\n"
                else:
                    suggestion += "I don't have enough information about room: " +str(rm) + ".  Sorry, you are on your own.\n"

        if (len(suggestion))<1:
            suggestion="KB Doesn't Have Enough Information to Help--Sorry"

        print(suggestion)


