#!/usr/bin/python

"""
Outputs a gnuplot graph with a parsed plan of a PostgreSQL
"EXPLAIN (FORMAT JSON)" SQL queries.

Sample usage:

psql -A -t -c 'EXPLAIN (FORMAT JSON) SELECT * FROM table_name' |
    ./json_parse.py |
    xdot
"""

import json

def to_dot_node(n, f):
    s = ""
    for k, v in n.items():
        if isinstance(v, list):
            continue
        s += ("%s: %s\\n" % (k, v))
    children = [to_dot_node(c, f) for c in n.get('Plans', [])]
    for child in children:
        s1 = s.replace('"', '\\"')
        s2 = child[0].replace('"', '\\"')
        f.write('"%s" -- "%s";\n' % (s1, s2))
    return s, children

def to_dot(s, f):
    j = json.loads(s)
    if len(j) != 1 and j.keys() != 'Plan':
        raise ValueError("Doesn't look like a JSON plan.")
    f.write("graph {")
    n = to_dot_node(j[0]['Plan'], f)
    f.write("}")

if __name__ == '__main__':
    import sys
    to_dot(sys.stdin.read(), sys.stdout)
