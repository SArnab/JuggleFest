JuggleFest
==========

A Python solution to the Juggle Fest problem presented on CodeEval: https://www.codeeval.com/open_challenges/88/

My implementation is a variation of the Gale-Shapely algorithm. A juggler is assigned to a circuit based on the order of preference. If the preferred circuit is already full, the fitness of the juggler is compared to that of the least fit juggler already assigned to the circuit. If it is higher, than the jugglers are replaced and the weaker juggler is again free to be assigned elsewhere.

Should the replacement not occur, the preference is dropped and the next preferred circuit is attempted. If all preferences fail, the juggler is assigned a random circuit from the remaining options.

The output is the sum of the juggler indexes assigned to circuit 1970 (as per Yodle's specifications).
