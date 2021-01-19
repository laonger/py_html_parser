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
assert node_list == [['div', [6, 7], {}, []]]

test_2_str = """
< div>
    <div>
        <br />
    </div>
</div>
"""

node_list = main.node_tree(test_2_str)
assert node_list == [['div', [7, 44], {}, [['div', [17, 37], {}, [['br', [32, 32], {}, []]]]]]]

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
assert node_list == [['div', [7, 109], {}, [['div', [17, 89], {}, [['br', [32, 32], {}, []], ['img', [61, 61], {'src': 'aldskjf'}, []], ['br', [67, 67], {}, []], ['a', [79, 80], {}, []]]], ['a', [103, 104], {}, []]]]]

test_4_str = """
<div class="nnn" id="ddd" style='ss:aa;' >
<a>
<br/>
<br/ >
</a>
< /div>
"""
t = time.time()
node_list = main.node_tree(test_3_str)
print((time.time()-t)*1000)
print(node_list)

