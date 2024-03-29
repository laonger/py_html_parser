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

s = """//div[@class="sss:'111'"][@id="jjj:'222'"]"""
result = xpath.path_parser(s)
assert result == [['div', 3, {'class': "sss:'111'", 'id':"jjj:'222'"}]]

s = """//div[@class="sss:'111'"]/div[@id='jjj']"""
result = xpath.path_parser(s)
assert result == [['div', 3, {'class': "sss:'111'"}], ['div', 2, {'id': "jjj"}]]

s = """div[@class="sss:'111'"]/div[@id='jjj']/a"""
result = xpath.path_parser(s)
assert result == [['div', 1, {'class': "sss:'111'"}], ['div', 2, {'id': "jjj"}], ['a', 2, {}]]

s = """//div[@class="sss:'111'"][@id="jjj:'222'"]/a"""
result = xpath.path_parser(s)
assert result == [['div', 3, {'class': "sss:'111'", 'id': "jjj:'222'"}], ['a', 2, {}]]



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


node_tree = [
    ['div', [7, 109], {}, [
        ['div', [17, 95], {}, [
            ['div', [22, 89], {}, [
                ['br', [32, 32], {}, []],
                ['img', [61, 61], {'src': 'aldskjf'}, []],
                ['br', [67, 67], {}, []],
                ['a', [79, 80], {}, []]
            ]],
            ['a', [103, 104], {}, []]
        ]],
    ]],
    ['div', [115, 116], {'id': 'jjj'}, [
        ['br', [84, 67], {}, []],
        ['a', [79, 99], {}, []]
    ]],
]

result = xpath.pickup(node_tree, "//div/a")
assert result == [['a', [79, 99], {}, []], ['a', [103, 104], {}, []], ['a', [79, 80], {}, []]]
result = xpath.pickup(node_tree, "/div//div/a")
assert result == [['a', [103, 104], {}, []], ['a', [79, 80], {}, []]]
result = xpath.pickup(node_tree, "/div/br")
assert result == [['br', [84, 67], {}, []]]

result = xpath.pickup(node_tree, "/div[@id='jjj']/a")
assert result == [['a', [79, 99], {}, []]]

