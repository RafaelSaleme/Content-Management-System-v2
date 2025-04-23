# Content-Management-System-v2

For the second part of the course the code was refactored using creation patterns

In this version was used the Factory Method in 2 instances

1. EntityFactory: Responsible for Author and Category
2. ArticleFactory: Responsible for the Articles

The idea of making 2 factories was to avoid having a contextual entity, the articles, and independent entities,
authors and categories in the same factory.

Doing so also makes it easier to evolve the ArticleFactory individually with new funtionalities.
