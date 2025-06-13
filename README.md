# Solr "Query Parser as a Service" Proof of Concept

Custom query parsers in Solr are tricky. This project (sketch?) is an exploration of implementing a custom query parser without having to write Java (or a JavaCC grammar), compile and configure the module, etc.

Instead, the idea is to serve a parser that takes a string in a custom query language and returns a query in Solr's JSON Query DSL.

The script in main.py uses Lark to create a parser based on a grammar of a custom query syntax and serves that parser using FastAPI

## Example

```bash
$ curl -X 'POST' \
        'http://localhost:8000/parse/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
    "text": "+hello ~silly ~world"
  }'
{"query":{"bool":{"must":[{"lucene":{"query":"hello"}}],"should":[{"lucene":{"query":"silly"}},{"lucene":{"query":"world"}}]}}}
```
