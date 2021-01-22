#!/usr/bin/env pypy3

import time

import xpath

s = """div"""
result = xpath.path_parser(s)
assert result == [['div', 1, {}]]

s = """/div"""
result = xpath.path_parser(s)
assert result == [['div', 2, {}]]

s = """//div"""
result = xpath.path_parser(s)
assert result == [['div', 3, {}]]

s = """//div/div"""
result = xpath.path_parser(s)
assert result == [['div', 3, {}], ['div', 2, {}]]

s = """//div[@class="sss:'111'"]"""
result = xpath.path_parser(s)
assert result == [['div', 3, {'class': "sss:'111'"}]]

s = """//div[@class="sss:'111'"]/div[@id='jjj']"""
result = xpath.path_parser(s)
assert result == [['div', 3, {'class': "sss:'111'"}], ['div', 2, {'id': "jjj"}]]

s = """div[@class="sss:'111'"]/div[@id='jjj']/a"""
result = xpath.path_parser(s)
assert result == [['div', 1, {'class': "sss:'111'"}], ['div', 2, {'id': "jjj"}], ['a', 2, {}]]





node_tree = [
    ['div', [7, 109], {}, [
        ['div', [17, 89], {}, [
            ['br', [32, 32], {}, []],
            ['img', [61, 61], {'src': 'aldskjf'}, []],
            ['br', [67, 67], {}, []],
            ['a', [79, 80], {}, []]
        ]],
        ['a', [103, 104], {}, []]
    ]],
    ['div', [115, 116], {'id': 'jjj'}, []],
]

cmd = xpath.path_parser("/div")[0]
result = xpath.cmd_2(node_tree[0][3], cmd)
assert result == [['div', [17, 89], {}, [['br', [32, 32], {}, []], ['img', [61, 61], {'src': 'aldskjf'}, []], ['br', [67, 67], {}, []], ['a', [79, 80], {}, []]]]]

cmd = xpath.path_parser("/div[@id='jjj']")[0]
result = xpath.cmd_2(node_tree, cmd)
assert result == [['div', [115, 116], {'id': 'jjj'}, []]]


cmd = xpath.path_parser("//a")[0]
result = xpath.cmd_3(node_tree, cmd)
assert result == [['a', [79, 80], {}, []], ['a', [103, 104], {}, []]]

#result = xpath.pickup(node_tree, "//a")
#assert result == [['a', [79, 80], {}, []], ['a', [103, 104], {}, []]]
#
#result = xpath.pickup(node_tree, "/div[@id='jjj']")
#assert result == [['div', [115, 116], {'id': 'jjj'}, []]]

print('#############################')
cmd_list = xpath.path_parser("//div/div")
result = xpath.aaaa(node_tree, cmd_list)
print(result)
