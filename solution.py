import sys
import re
from random import randint

circuits = {}
jugglers = {}

def main():
	# Build the list of circuits and jugglers
	fh = open(sys.argv[1],"r")
	for line in fh.readlines():
		if(line == "\n"):
			continue
		if(line[0] == "C"):
			values = re.findall(r'C C(\d+) H:(\d+) E:(\d+) P:(\d+)',line)
			circuits[int(values[0][0])] = Circuit(values[0][0],values[0][1],values[0][2],values[0][3])
		else:
			values = re.findall(r'J J(\d+) H:(\d+) E:(\d+) P:(\d+) C(\d+),C(\d+),C(\d+)',line)
			jugglers[int(values[0][0])] = Juggler(values[0][0],values[0][1],values[0][2],values[0][3],values[0][4],values[0][5],values[0][6])
	fh.close()

	jugglerLength = len(jugglers);
	circuitLength = len(circuits);

	jugglersPerCircuit = jugglerLength / circuitLength;
	currentIndex = 0;

	while(len(jugglers) > 0):
		while((currentIndex in jugglers) == False):
			currentIndex = randint(0,jugglerLength-1);

		juggler = jugglers[currentIndex];

		for i in range(juggler.lastPrefIndex,len(juggler.preferences)):
			#print "Processing preference index %d for Juggler %d" % (i,juggler.index);
			juggler.lastPrefIndex = i;
			preferredCircuit = circuits[juggler.preferences[i]];
			juggler.currentFit = (preferredCircuit.hVal * juggler.hVal)+(preferredCircuit.eVal * juggler.eVal)+(preferredCircuit.pVal * juggler.pVal)
			
			if(len(preferredCircuit.assignedJugglers) < jugglersPerCircuit):
				# There's Room. Hop Right In
				#print "Juggler %d assigned to circuit %s because there was space." % (juggler.index,preferredCircuit.index)
				preferredCircuit.assignedJugglers[juggler.index] = juggler;
				juggler.isMatched = True;
				del jugglers[juggler.index];
				break;
			else:
				minimumFit = min(map(lambda (k,juggler): juggler.currentFit,preferredCircuit.assignedJugglers.iteritems()))
				if(juggler.currentFit > minimumFit):
					# Remove the weaker guy
					minimumJuggler = filter(lambda (k,juggler): juggler.currentFit == minimumFit,preferredCircuit.assignedJugglers.iteritems())[0][1];
					minimumJuggler.isMatched = False;
					jugglers[minimumJuggler.index] = minimumJuggler;
					del preferredCircuit.assignedJugglers[minimumJuggler.index];
					#print "Juggler %d was removed from circuit %s" % (minimumJuggler.index,preferredCircuit.index)
					# Assign the more fit guy
					juggler.isMatched = True;
					preferredCircuit.assignedJugglers[juggler.index] = juggler;
					del jugglers[juggler.index]
					#print "Juggler %d assigned to circuit %s" % (juggler.index,preferredCircuit.index)
					break;

		if(juggler.isMatched == False):
			#print "Juggler %d was unable to enter any of his preferred circuits" % (juggler.index)

			while(juggler.isMatched == False):
				# Assign To A Random Circuit
				randomIndex = randint(0,circuitLength)
				while((randomIndex in circuits) == False):
					randomIndex = randint(0,circuitLength)
				randomCircuit = circuits[randomIndex];
				juggler.currentFit = (randomCircuit.hVal * juggler.hVal)+(randomCircuit.eVal * juggler.eVal)+(randomCircuit.pVal * juggler.pVal)

				if(len(randomCircuit.assignedJugglers) < jugglersPerCircuit):
					# There's Room. Hop In!
					#print "Assigning Juggler %d to random circuit %d" % (juggler.index,randomCircuit.index)
					randomCircuit.assignedJugglers[juggler.index] = juggler;
					juggler.isMatched = True;
					del jugglers[juggler.index];
				else:
					minimumFit = min(map(lambda (k,juggler): juggler.currentFit,randomCircuit.assignedJugglers.iteritems()))
					if(juggler.currentFit > minimumFit):
						# Remove the weaker guy
						minimumJuggler = filter(lambda (k,juggler): juggler.currentFit == minimumFit,randomCircuit.assignedJugglers.iteritems())[0][1];
						minimumJuggler.isMatched = False;
						jugglers[minimumJuggler.index] = minimumJuggler;
						del randomCircuit.assignedJugglers[minimumJuggler.index];
						#print "Juggler %d was removed from circuit %s" % (minimumJuggler.index,randomCircuit.index)
						# Assign the more fit guy
						juggler.isMatched = True;
						randomCircuit.assignedJugglers[juggler.index] = juggler;
						del jugglers[juggler.index]
						#print "Juggler %d assigned to random circuit %s" % (juggler.index,randomCircuit.index)
						break;

				
		currentIndex += 1;

	print sum(map(lambda (k,juggler): juggler.index,circuits[1970].assignedJugglers.iteritems()))

class Circuit:

	hVal = 0;
	eVal = 0;
	pVal = 0;
	assignedJugglers = {};

	def __init__(self,index,hVal,eVal,pVal):
		self.index = int(index);
		self.hVal = int(hVal);
		self.eVal = int(eVal);
		self.pVal = int(pVal);
		self.assignedJugglers = {};

class Juggler:

	index = 0;
	hVal = 0;
	eVal = 0;
	pVal = 0;
	lastPrefIndex = 0;
	currentFit = 0;
	isMatched = False;

	def __init__(self,index,hVal,eVal,pVal,pref1,pref2,pref3):
		self.index = int(index);
		self.hVal = int(hVal);
		self.eVal = int(eVal);
		self.pVal = int(pVal);
		self.preferences = [int(pref1), int(pref2), int(pref3)];

main()