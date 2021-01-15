#!/usr/bin/env pypy3

import time
import main

test_tag_1_str = """
<div></div>
"""
result = main.pick_tag_name(test_tag_1_str)
assert result == (5, 'div', True, 0)

test_tag_2_str = """
< div >< / div>
"""
result = main.pick_tag_name(test_tag_2_str)
assert result == (7, 'div', True, 0)

test_tag_3_str = """
< div sss="/>sss" >< / div>
"""
result = main.pick_tag_name(test_tag_3_str)
print(result)
assert result == (13, 'div', False, 0)

test_tag_4_str = """
< / div    >
"""
result = main.pick_tag_name(test_tag_4_str)
assert result == (12, 'div', True, -1)

test_tag_5_str = """
< div / >
"""
result = main.pick_tag_name(test_tag_5_str)
assert result == (9, 'div', True, 1)

test_tag_6_str = """
< div/a >
"""
result = main.pick_tag_name(test_tag_6_str)
assert result == (9, 'div', True, 1)

test_tag_attr_1_str = """
class="nnn" id="ddd" style='ss:aa;' >
"""
result = main.pick_attrs(test_tag_attr_1_str)
assert result == (37, {'class': '"nnn"', 'id': '"ddd"', 'style': "'ss:aa;'"})

test_tag_attr_2_str = """
class="nnn" id="ddd />" style='ss:aa;' >
"""
result = main.pick_attrs(test_tag_attr_2_str)
assert result == (40, {'class': '"nnn"', 'id': '"ddd />"', 'style': "'ss:aa;'"})

test_tag_attr_3_str = """
class="nnn" id="ddd />" style='ss:aa; aa:"jjj"' />
"""
result = main.pick_attrs(test_tag_attr_3_str)
assert result == (50, {'class': '"nnn"', 'id': '"ddd />"', 'style': '\'ss:aa; aa:"jjj"\''})

test_1_str = """
<div>
</div>
"""
node_list = main.node_tree(test_1_str)
print(node_list)
assert node_list == [['div', [6, 0], {}, []]]

test_2_str = """
< div>
    <div>
        <br />
        <img src="aldskjf"/><br />
        <a> </a>
    </div>
    <a> </a>
</div>
"""
print('######################################')
t = time.time()
node_list, n = main.node_tree(test_2_str)
print((time.time()-t)*1000)
print(node_list)
assert node_list == [['div', [7, 45], {}, [['div', [13, 29], {}, [['a', [17, 22], {}, []]]], ['a', [33, 38], {}, []]]]]

test_3_str = """
<div class="nnn" id="ddd" style='ss:aa;' >
<a>
<br/>
<br/ >
</a>
< /div>
"""
#t = time.time()
#print(main.node_tree(test_3_str))
#print((time.time()-t)*1000)

