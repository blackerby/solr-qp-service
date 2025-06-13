# Solr "Query Parser as a Service" Proof of Concept

Custom query parsers in Solr are tricky. This sketch of a project explores implementing a custom query parser without having to write Java (or a [JavaCC](https://javacc.github.io/javacc/) grammar), compile and configure the module, etc.

Instead, the idea is to serve a parser that takes a string in a custom query language and returns a query in Solr's [JSON Query DSL](https://solr.apache.org/guide/solr/latest/query-guide/json-query-dsl.html).

The script in main.py uses [Lark](https://lark-parser.readthedocs.io/en/latest/index.html) to create a parser based on a grammar of a custom query syntax and serves that parser using [FastAPI](https://fastapi.tiangolo.com/).

## Example

Start the server:
```bash
$ fastapi dev main.py
```

Send a query string:
```bash
$ curl -X 'POST' \
        'http://localhost:8000/parse/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
    "text": "+hello ~silly +3w(world, wonder)"
  }'

{'query': {'bool': {'must': [{'lucene': {'query': 'hello'}},
                             {'surround': {'query': '3w(world, wonder)'}}],
                    'should': [{'lucene': {'query': 'silly'}}]}}}
```
