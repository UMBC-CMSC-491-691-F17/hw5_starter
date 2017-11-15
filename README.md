# Homework Five: Writing SPARQL Queries

out Wednesday 2017-11-13, due Monday 2016-11-25

This homework will give you some experience in using the RDF query language SPARQL to access the stereotypical linked open data collection, DBpedia.

SPARQL is a relatively straightforward query language for RDF data that will seem familiar to people to know SQL. It does have a number of unique features that stem from the RDF model. What is different, though, is how we have to approach querying a large semi-structured collection like DBpedia. A typical relational database has a small number of tables each with a fixed number of columns and every row in table has a value for each column. The database schema is thus uniform and relatively small.

This repository has a stub for each of the queries you have to write with a name like q??.txt. Edit each stub to be a working query, verifying that it works using a web based sparql client like http://live.dbpedia.org/sparql or yasgui or just use the python script sparql.py to run the query and produce output files.

A standard public sparql endpoint for DBpedia is http://live.dbpedia.org/sparql which is a public service offered by Open Link Software. Their triple store technology is very good, has both a commercial and open source versions and supports most (but not all) of the SPARQL 1.1 standard. We recommend using this rather than http://dbpedia.org/sparql since it has more data and it more up-to-date.

When you are done, you can rerun all of your queries with a command like python sparql.py q*.txt. Add the *.html and *.txt files to your repository, then commit all of the *.txt, *.txt.json and *.txt.html files and push them back to the master on github.

