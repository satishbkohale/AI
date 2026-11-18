% Experiment 1 - Prolog (run with: swipl exp1_prolog.pl)

% ---------- Example 1: likes / friends ----------
likes(mary, pizza).
likes(john, pizza).
likes(john, pasta).
friends(X, Y) :- likes(X, Z), likes(Y, Z), X \= Y.

% ---------- Example 2: family tree ----------
parent(john, mary).
parent(jane, mary).
parent(john, bob).
parent(jane, bob).
parent(mary, alice).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(Z, Y), ancestor(X, Z).

% ---------- INPUT QUERIES (type at the ?- prompt) ----------
% ?- friends(mary, john).     % true
% ?- sibling(mary, bob).      % true
% ?- ancestor(john, alice).   % true
% ?- ancestor(X, alice).      % X = mary ; X = john ; X = jane
