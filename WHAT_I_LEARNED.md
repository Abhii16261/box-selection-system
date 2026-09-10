# What I Learned

## Hardest part

The hardest part for me was getting the venv file in the right place. I kept
accidentally committing it and had to keep fixing it in git.

## What I learned about Django

I learned about Django more this time. I understood how the models, admin
panel, and the box recommendation logic worked together.

## The test bug I found

I worked on the test that failed. I learned how to fix it. The test expected
the small box but the algorithm picked the medium box. I found out the Book
product was too long to fit in the small box, so the algorithm was actually
correct and my test was wrong. I fixed the test.

## Git

First I fixed venv and db.sqlite3 being tracked by git. I learned that adding
something to .gitignore does not remove it from git if it was already
committed before - you have to use git rm --cached to actually untrack it.
This happened to me more than once before I understood it properly.

## What I would do differently

Next time I would check my .gitignore file and make sure it is working
correctly before my very first git commit, so I don't have to fix venv and
db.sqlite3 being tracked again and again.