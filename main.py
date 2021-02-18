#!/usr/bin/env pypy3

import copy

import utils

# TODO 处理空格，换行符，处理<br/>换行，<p>换行


def new_node():
    """docstring for new_node"""
    return [
        '',     # 0, tag_name
        [-1, -1, -1, -1], # 0-tag_start(<), 1-block_start, 2-block_end, 3-end_tag_end;  tag_end = blog_start-1, end_tag_start = block_end +1
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
    # 因为s的起始位置就是cur_n的下一位，所以返回的时候要+1
    return n+1, tag_name, tag_end, block_close

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
    # 因为s的起始位置就是cur_n的下一位，所以返回的时候要+1
    return n+1, d, block_close

def node_tree(s):
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
    tag_list = []
    cur = ''
    other = ''
    node_list = []
    while n < len(s):
        attrs = {}
        tag_name = ''
        node = None
        pre_n, n = utils.n_increase(n, 1)
        if n == len(s)-1:
            cur, other = s[n], ''   # TODO
        elif n == len(s):
            break                   # TODO
        else:
            cur, other = s[n], s[n+1:]
        if cur == '<':
            tag_start_n = n

            delta_n, tag_name, tag_end, block_close = pick_tag_name(other)
            pre_n, n = utils.n_increase(n, delta_n)
            if not tag_end:
                #n += 1
                #cur, other = s[n], s[n+1:]
                other = s[n:]
                delta_n, attrs, block_close = pick_attrs(other)
                pre_n, n = utils.n_increase(n, delta_n)
            end_tag_end_n = n+1

            if block_close <0:         # 如果是结束block标记, 非独立tag   
                node = tag_list.pop()
                while node[0] != tag_name:
                    node = tag_list.pop()
                    if not tag_list and node[0] != tag_name:
                        raise # 如果出现莫名奇妙的结束tag，则忽略
                node[1][2] = pre_n
                node[1][3] = end_tag_end_n
            elif block_close >0: # 如果是一个独立的tag
                node = new_node()
                node[0] = tag_name
                node[1][0] = tag_start_n
                node[1][1] = n+1
                node[1][2] = n+1
                node[1][3] = end_tag_end_n
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
                node[1][0] = tag_start_n
                node[1][1] = n+1
                node[2] = attrs
                tag_list.append(node)
                continue
    return node_list

def text(html_string, node):
    """docstring for text"""
    result = []
    anchor_list = []
    temp = [node]
    html_string = html_string[node[1][0]:node[1][3]]
    start_n = node[1][0]
    while temp:
        n = temp.pop(0)
        if n[3]:
            temp.extend(n[3])
        if n[1][0] != n[1][1] and n[1][0] != -1 and n[1][1] != -1:
            anchor_list.append((n[1][0], n[1][1]))
        if n[1][2] != n[1][3] and n[1][2] != -1 and n[1][3] != -1:
            anchor_list.append((n[1][2], n[1][3]))

    anchor_list.sort()
    anchor = anchor_list.pop(0)
    for n, i in enumerate(html_string):
        n += start_n
        if n > anchor[1] and anchor_list:
            anchor = anchor_list.pop(0)
        if n >= anchor[0] and n <= anchor[1]:
            continue
        #if i in utils.BLANK:
        #    continue
        result.append(i)
    return ''.join(result)

def get_attr(node, attr_key):
    """docstring for get_attr"""
    return node[2].get(attr_key)

