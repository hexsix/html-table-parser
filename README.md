# html table parser

## python version

python 3.5+

## example of usages

```python
from pprint import pprint
from html_table_parser import HTMLTableParser

html = """html code here"""
p = HTMLTableParser()
p.feed(html)
pprint(p.tables)
```

## Description

相比 schmijos 的 parser，本版本可以解析套娃和 table 所在的位置（line number & column number）

## Thanks

[schmijos/html-table-parser-python3]("https://github.com/schmijos/html-table-parser-python3")
