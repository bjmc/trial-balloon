# Democracy Club interview task

This is a task designed to see how you think through complex problems.

The task is typical of some higher level problems we think about at DC, and
doesn't have a single correct solution.

There are some drawbacks that we understand about any code test: in a typical
job complex tasks are in context of familiar applications or domains. You will
normally have a good idea of how the task fits into other tasks, and you will
know more about how the code might be used and maintained over time.

We understand this and will take the limitations of the test into account as we
read over the implementations.

We do expect high quality code that is tested. It's better to complete a part of
the project with high quality code than to technically finish the entire test
without any form of testing in place. We have provided a working set of
tests to help you with this.

It would be nice to at least have a working proof of concept, but as important
is some description of how you're thinking about the problem and what you might
do differently if you had longer or could change some parameters.

## The background

In this repo you will see a python file `src/main.py` and some JSON in
`sandbox_responses`.

`main.py` is an example consumer of one of the APIs that we
maintain. The sandbox JSON represents example responses from the API.

These objects represent the information we know about elections that are taking
place. The set that is returned may be determined by a variety of factors, eg
date or location.

The examples are important as there are many cases that only show up in the live
API occasionally, for example, we need to ensure that our code works for general
elections, however there are limited times when the actual API will show one.

For some of our data (polling stations) we only have content in the database
just before elections, and never return a station for a postcode if there aren’t
upcoming elections. This means we need to rely on the examples rather than live
or staging APIs.

You don't need to understand everything about the response, however the most
important thing to know is that the valid (non-error) data returned can change
depending on a number of factors:

For a given query, there can be any number of ballots from 0 to ~4 over a number
of dates.

* For each ballot, there can be any number of candidates from 0 to 10 or more
* For each ballot there can be exactly one of a known number of voting systems
* For each date there can be a polling station known, or not
* Every object (including sub-objects) have a number of additional fields

In short, the API response is a complex set of nested objects.

If you did want to learn more about the data model, you can do so here:

https://developers.democracyclub.org.uk/api/v1/

This isn't really part of the test though, and you can work on the problem 
without a full understanding of the domain. 

## The problem

The sandbox responses are duplicated across projects and managed in an ad hoc 
fashion as separate json file. The responses are used in a number of ways:

* As fixtures in tests across different projects
* As mock data used by projects that showcase our work between elections (e.g 
  to see feature X, type in postcode Y)

Because they are complex, adding new fields can be laborious, and it can be hard
to validate that the sample data is actually the same as the live API would
produce.

We need a better way to manage this data that allows us to add more fields, add
more example scenarios, and ensure it is valid output. This system needs to work
with more than one internal project and ideally help us with documentation.

## The task

We want to know how you would go about solving the problem, both in terms of the
code you'd write and the way you would maintain a common, validated data
structure over more than one project.

We're looking for some working code that provides a minimum example with a
nested data structure like the sandbox examples. You don't have to implement the
entire structure, as we'd rather have a more complete solution on a smaller
model.

The code should be usable for testing `main.py`’s functionality. Changing `main.py`
to be easier to test is an option, as the priority is maintainability of code
and data structures across projects.

As well as code, we would like your thoughts on the tradeoffs your approach
would have in real projects. Ideally you would include some idea of alternative
approaches and why you didn't pick them

You should submit your answer via a pull request to this repo, with code in the
commit and commentary in the PR description.
