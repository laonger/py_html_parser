#!/usr/bin/env pypy3

import utils


def new_node():
    """docstring for new_node"""
    return [
        '',     # 0, tag_name
        [0, 0], # 1, block start end
        {},     # 2, attrs
        [],     # 3, children
    ]


def pick_tag_name(s):
    """docstring for pick_tag_name"""
    tag_end = False
    block_close = 0         # -1, /在tag name左边，1，/在tag name右边（"</div>, <br/>'）
    tag_name = ''
    quot = ''
    tag_name_temp = []
    key_temp = []
    key = ''
    for n, i in enumerate(s):
        if i == '<' and not tag_name_temp:  # 抛弃掉第一个<, 不可能出现"   <div"这种情况
            continue
        if i == '>':
            tag_end = True
            break
        if i in utils.BLANK:
            if tag_name_temp:
                tag_name = ''.join(tag_name_temp)
                break
            continue
        elif i == '/':
            block_close = -1 if not tag_name_temp else 1
            tag_end = True
            continue
        else:
            tag_name_temp.append(i)
    if not tag_name:
        tag_name = ''.join(tag_name_temp)
    if block_close:         # 如果出现 "< / div      >"这种情况，把游标挪到">"的位置
        while i != '>':
            n +=1
            i = s[n]
    return n, tag_name, tag_end, block_close

def pick_attrs(s):
    """docstring for pick_attrs"""
    d = {}
    l =[]
    key = ''
    quot = ''
    block_close = 0
    for n, i in enumerate(s):
        if i in utils.BLANK and not quot:
            continue
        if i != '=':
            l.append(i)
        else:
            key = ''.join(l)
            l = []

        if i in utils.QUOT:
            if not quot:
                quot = i
            elif i == quot: # 引号结束
                d[key] = utils.remove_quot(''.join(l))
                l = []
                key = ''
                quot = ''
        if i == '/' and not quot:
            block_close = 1
        if i == '>' and not quot:
            break
    return n, d, block_close

def node_tree(s, node_list=None, tag_list=None):
    """docstring for c
    [
        [
            tag_name,
            [block_start_int, block_end_int],
            attrs,      # dict
            [
                child_1,
                child_2
            ]
        ],
    ]
    """
    n = -1
    pre_n = n
    tag_name = ''
    if tag_list is None:
        tag_list = []
    cur = ''
    other = ''
    attrs = {}
    if node_list is None:
        node_list = []
    node = None
    while n < len(s):
        pre_n, n = utils.n_increase(n, 1)
        if n == len(s)-1:
            cur, other = s[n], ''   # TODO
        elif n == len(s):
            break                   # TODO
        else:
            cur, other = s[n], s[n+1:]
        if cur == '<':
            delta_n, tag_name, tag_end, block_close = pick_tag_name(other)
            pre_n, n = utils.n_increase(n, delta_n)
            if not tag_end:
                n += 1
                cur, other = s[n], s[n+1:]
                delta_n, attrs, block_close = pick_attrs(other)
                pre_n, n = utils.n_increase(n, delta_n)

            if block_close <0:         # 如果是结束block标记    
                node = tag_list.pop()
                if tag_name != node[0]:     # 如果出现莫名奇妙的结束tag，则忽略
                    continue
                node[1][1] = pre_n
                continue
            elif block_close >0: # 如果是一个独立的tag
                node = new_node()
                node[0] = tag_name
                node[1][0] = n+2
                node[1][1] = n+2
                node[2] = attrs
                if tag_list:
                    tag_list[-1][3].append(node)
                else:
                    node_list.append(node)
                continue
            else:
                node = new_node()
                if tag_list:
                    tag_list[-1][3].append(node)
                else:
                    node_list.append(node)
                node[0] = tag_name
                node[1][0] = n+2
                node[2] = attrs
                tag_list.append(node)
                continue
    return node_list

