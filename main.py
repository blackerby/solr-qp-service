from lark import Lark, Transformer, Tree
from fastapi import FastAPI
from pydantic import BaseModel


grammar = r"""
    query: lucene
         | bool
         | surround

    lucene : WORD
    bool : (should | must)+
    should : "~" (lucene | bool | surround)
    must : "+" (lucene | bool | surround)
    surround : distance distop "(" WORD ", " WORD ")"
    distance : INT 
    distop : within | near
    within : "w" | "W"
    near : "n" | "N"

    %import common.WORD
    %import common.INT
    %import common.WS

    %ignore WS
"""


class TreeToJson(Transformer):
    def query(self, tree):
        (q,) = tree
        return {"query": q}

    def bool(self, tree):
        must = []
        should = []
        for branch in tree:
            if branch.data == "must":
                must.extend(branch.children)
            if branch.data == "should":
                should.extend(branch.children)
        return {"bool": {"must": must, "should": should}}

    def lucene(self, tree):
        q = tree[0].value
        return {"lucene": {"query": q}}

    def surround(self, tree):
        inner = []
        for branch in tree:
            if isinstance(branch, Tree):
                if branch.data == "distance":
                    distance = branch.children[0].value
                if branch.data == "distop":
                    leaf = branch.children[0].data
                    if leaf == "within":
                        distop = "w"
                    else:
                        distop = "n"
            else:
                inner.append(branch.value)
        inner = ", ".join(inner)
        q = f"{distance}{distop}({inner})"
        return {"surround": q}


parser = Lark(grammar, start="query", parser="lalr", transformer=TreeToJson())

app = FastAPI()


class Query(BaseModel):
    text: str


@app.post("/parse/")
async def parse(query: Query):
    tree = parser.parse(query.text)
    result = TreeToJson().transform(tree)
    return result
