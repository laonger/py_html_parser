#!/usr/bin/env pypy3

import time
from . import nodes as main

#import httpx
#t = httpx.get('https://www.w3schools.com/html/html_intro.asp')
#node_list = main.node_tree(t.content.decode('utf-8'))
#print(node_list)


test_tag_1_str = """
<div></div>
"""
result = main.pick_tag_name(test_tag_1_str)
assert result == (5, 'div', True, 0)

test_tag_2_str = """
< div >< / div>
"""
result = main.pick_tag_name(test_tag_2_str)
assert result == (6, 'div', False, 0)

test_tag_3_str = """
< div sss="/>sss" >< / div>
"""
result = main.pick_tag_name(test_tag_3_str)
assert result == (6, 'div', False, 0)

test_tag_4_str = """
< / div    >
"""
result = main.pick_tag_name(test_tag_4_str)
assert result == (12, 'div', True, -1)

test_tag_5_str = """
< div / >
"""
result = main.pick_tag_name(test_tag_5_str)
assert result == (6, 'div', False, 0)

# TODO 此为错误格式，应该报错？
test_tag_6_str = """
< div/a >
"""
result = main.pick_tag_name(test_tag_6_str)
assert result == (9, 'diva', True, 1)

test_tag_attr_1_str = """
class="nnn" id="ddd" style='ss:aa;' >
"""
result = main.pick_attrs(test_tag_attr_1_str)
assert result == (37, {'class': 'nnn', 'id': 'ddd', 'style': 'ss:aa;'}, 0)

test_tag_attr_2_str = """
class="nnn" id="ddd />" style='ss:aa;' >
"""
result = main.pick_attrs(test_tag_attr_2_str)
assert result == (40, {'class': 'nnn', 'id': 'ddd />', 'style': "ss:aa;"}, 0)

test_tag_attr_3_str = """
class="nnn" id="ddd />" style='ss:aa; aa:"jjj"' />
"""
result = main.pick_attrs(test_tag_attr_3_str)
assert result == (50, {'class': 'nnn', 'id': 'ddd />', 'style': 'ss:aa; aa:"jjj"'}, 1)

test_1_str = """
<div>
</div>
"""
node_list = main.node_tree(test_1_str)
assert node_list == [('div', [1, 6, 7, 12], {}, [])]


test_2_str = """ < div>
    <div>
        <br />
    </div>
</div>
"""

node_list = main.node_tree(test_2_str)
assert node_list == [('div', [1, 7, 44, 49], {}, [('div', [12, 17, 37, 42], {}, [('br', [26, 32, 32, 31], {}, [])])])]


test_3_str = """
< div>
    <div>
        <br />
        <img src="aldskjf"/><br />
        <a> </a>
    </div>
    <a> </a>
</div>
"""
node_list = main.node_tree(test_3_str)

assert node_list == [('div', [1, 7, 109, 114], {}, [('div', [12, 17, 89, 94], {}, [('br', [26, 32, 32, 31], {}, []), ('img', [41, 61, 61, 60], {'src': 'aldskjf'}, []), ('br', [61, 67, 67, 66], {}, []), ('a', [76, 79, 80, 83], {}, [])]), ('a', [100, 103, 104, 107], {}, [])])]



test_4_str = """
<div class="nnn" id="ddd" style='ss:aa;' >
<a>
<br/>
<br/ >
</a>
< /div>
"""
t = time.time()
node_list = main.node_tree(test_4_str)
assert node_list == [('div', [1, 43, 66, 72], {'class': 'nnn', 'id': 'ddd', 'style': 'ss:aa;'}, [('a', [44, 47, 61, 64], {}, [('br', [48, 53, 53, 52], {}, []), ('br', [54, 60, 60, 59], {}, [])])])]

test_3_str = """
        <br />
        ooooo
        <img src="aldskjf"/>
        <a>jjjjj</a>
"""
node_list = main.node_tree(test_3_str)
assert node_list == [('br', [9, 15, 15, 14], {}, []), ('img', [38, 58, 58, 57], {'src': 'aldskjf'}, []), ('a', [67, 70, 75, 78], {}, [])]


test_3_str = """< div id="nnnn"><div>
        <br />
        ooooo
        <img src="aldskjf"/><br />
        <a>jjjjj</a>
    </div>
    <a> </a>
</div>
"""
t = time.time()
# 0.8863420486450195
for i in range(100000):
    node_list = main.node_tree(test_3_str)
print(time.time()-t)
t = time.time()
for i in range(100000):
    node_list = main.node_tree_a(test_3_str)
print(time.time()-t)
assert node_list == [('div', [0, 16, 131, 136], {'id': 'nnnn'}, [('div', [16, 21, 111, 116], {}, [('br', [30, 36, 36, 35], {}, []), ('img', [59, 79, 79, 78], {'src': 'aldskjf'}, []), ('br', [79, 85, 85, 84], {}, []), ('a', [94, 97, 102, 105], {}, [])]), ('a', [122, 125, 126, 129], {}, [])])]

test_3_str = """
< div>
nnnnnn
    <div>
        <br />
        ooooo
        <img src="aldskjf"/><br />
        <a>jjjjj</a>
    </div>
    <a> </a>
</div>
"""
node_list = main.node_tree(test_3_str)
print(node_list)
node = ['a', [97, 100, 105, 109], {}, []]
text = main.text(test_3_str, node)
print(text)

node = ['div', [19, 24, 114, 120], {}, [['br', [33, 39, -1, -1], {}, [['img', [62, 82, 82, 82], {'rc': 'aldskjf'}, []], ['br', [82, 88, -1, -1], {}, [['a', [97, 100, 105, 109], {}, []]]]]]]]
text = main.text(test_3_str, node)
print(text)



