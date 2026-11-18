
% Experiment 1 - Prolog Facts and Rules

% Example 1: Likes and Friends

likes(mary, pizza).
likes(john, pizza).
likes(john, pasta).

friends(X, Y) :-
    likes(X, Z),
    likes(Y, Z),
    X \= Y.

% Example 2: Family Tree

parent(john, mary).
parent(jane, mary).
parent(john, bob).
parent(jane, bob).
parent(mary, alice).

% Sibling Rule
sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y.

% Ancestor Rules
ancestor(X, Y) :-
    parent(X, Y).

ancestor(X, Y) :-
    parent(Z, Y),
    ancestor(X, Z).

% Example Queries:
% ?- friends(mary, john).
% ?- sibling(mary, bob).
% ?- ancestor(john, alice).
% ?- ancestor(X, alice).
