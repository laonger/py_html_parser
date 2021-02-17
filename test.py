#!/usr/bin/env pypy3

import time
import main

#import httpx
#t = httpx.get('https://www.w3schools.com/html/html_intro.asp')
#node_list = main.node_tree(t.content.decode('utf-8'))
#print(node_list)


test_tag_1_str = """
<div></div>
"""
result = main.pick_tag_name(test_tag_1_str)
assert result == (6, 'div', True, 0)

test_tag_2_str = """
< div >< / div>
"""
result = main.pick_tag_name(test_tag_2_str)
assert result == (7, 'div', False, 0)

test_tag_3_str = """
< div sss="/>sss" >< / div>
"""
result = main.pick_tag_name(test_tag_3_str)
assert result == (7, 'div', False, 0)

test_tag_4_str = """
< / div    >
"""
result = main.pick_tag_name(test_tag_4_str)
assert result == (13, 'div', True, -1)

test_tag_5_str = """
< div / >
"""
result = main.pick_tag_name(test_tag_5_str)
assert result == (7, 'div', False, 0)

# TODO 此为错误格式，应该报错？
test_tag_6_str = """
< div/a >
"""
result = main.pick_tag_name(test_tag_6_str)
assert result == (10, 'diva', True, 1)

test_tag_attr_1_str = """
class="nnn" id="ddd" style='ss:aa;' >
"""
result = main.pick_attrs(test_tag_attr_1_str)
assert result == (38, {'class': 'nnn', 'id': 'ddd', 'style': 'ss:aa;'}, 0)

test_tag_attr_2_str = """
class="nnn" id="ddd />" style='ss:aa;' >
"""
result = main.pick_attrs(test_tag_attr_2_str)
assert result == (41, {'class': 'nnn', 'id': 'ddd />', 'style': "ss:aa;"}, 0)

test_tag_attr_3_str = """
class="nnn" id="ddd />" style='ss:aa; aa:"jjj"' />
"""
result = main.pick_attrs(test_tag_attr_3_str)
assert result == (51, {'class': 'nnn', 'id': 'ddd />', 'style': 'ss:aa; aa:"jjj"'}, 1)

test_1_str = """
<div>
</div>
"""
node_list = main.node_tree(test_1_str)
assert node_list == [['div', [1, 6, 7, 13], {}, []]]

test_2_str = """ < div>
    <div>
        <br />
    </div>
</div>
"""

node_list = main.node_tree(test_2_str)
assert node_list == [['div', [1, 7, 44, 50], {}, [['div', [12, 17, 37, 43], {}, [['br', [26, 32, -1, -1], {}, []]]]]]]


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
assert node_list == [['div', [1, 7, 109, 115], {}, [['div', [12, 17, 89, 95], {}, [['br', [26, 32, -1, -1], {}, [['img', [41, 61, 61, 61], {'rc': 'aldskjf'}, []], ['br', [61, 67, -1, -1], {}, [['a', [76, 79, 80, 84], {}, []]]]]]]], ['a', [100, 103, 104, 108], {}, []]]]]

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
