% house each place holder in represented as color, nationality, beverage, candy, dog
houselist([house(_,_,_,_,_),
	house(_,_,_,_,_),
	house(_,_,_,_,_),
	house(_,_,_,_,_),
	house(_,_,_,_,_)]).

rules(H) :-
    member(house(red,englishmen,_,_,_), H),
    member(house(_,spaniard,_,_,dog), H),
    H = [house(_,norwegian,_,_,_),_,_,_,_],                          
    member(house(_,_,_,smarty, snail), H),
	nextto(house(white,_,_,_,_), house(green,_,_,_,_), H), 
    permutation([house(_,_,_,hershey,_), house(_,_,_,_,fox)], [X,Y]),
    nextto(X,Y, H),
    member(house(yellow,_,_,kitkat,_), H),
    permutation([house(_,norwegian,_,_,_), house(blue,_,_,_,_)], [Q,W]),
    nextto(Q, W, H),
    member(house(_,_,juice,snicker,_), H),
    member(house(_,japanese,_,milkyway,_), H),
    member(house(_,ukranian,tea,_,_), H),
    permutation([house(_,_,_,kitkat,_), house(_,_,_,_,horse)], [A,S]),
    nextto(A,S, H),
    member(house(green,_,coffee,_,_), H),
    H = [_,_,house(_,_,milk,_,_),_,_],                          
    member(house(_,_,_,_,zebra), H),
    member(house(_,_,water,_,_), H).

%might need to define some of these rules a little bit more
zebralive(Color) :-
    houselist(H),
	rules(H),
	member(house(Color,_,_,_,zebra), H).

drinkwater(Color) :-
    houselist(H),
	rules(H),
	member(house(Color,_,water,_,_), H).

listhouse(H) :-
    houselist(H),
    rules(H).