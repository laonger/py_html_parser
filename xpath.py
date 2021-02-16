#!/usr/bin/env pypy3

import copy
import utils


def new_cmd():
    """docstring for new_cmd"""
    return [
        '',
        1,
        {}
    ]

def path_parser(path):
    """
    [["tag_name", "pick_type", "attr"], ["tag_name", "pick_type", "attr"]]

    pick_type: {
        "div": 1,
        "/div": 2,
        "//div": 3
    }
    """
    n = -1
    length = len(path)
    result = []
    attr_key = ''
    quot = ''
    cmd = new_cmd()
    temp = []
    while n < length-1:
        n += 1
        cur, other = path[n], path[n+1:]
        if cur == '/'and not quot:
            if temp:
                cmd[0] = ''.join(temp)
                temp = []
                result.append(cmd)
                cmd = new_cmd()
            if other[0] == '/':
                cmd[1] = 3
                n +=1
            else:
                cmd[1] = 2
        elif cur == '[' and not quot:
            cmd[0] = ''.join(temp)
            temp = []
        elif cur == ']' and not quot:
            cmd[2][attr_key] = utils.remove_quot(''.join(temp))
            attr_key = ''
            temp = []
            result.append(cmd)
            cmd = new_cmd()
        elif cur == '=' and not quot:
            attr_key = utils.remove_quot(''.join(temp))
            temp = []
            continue
        elif cur in utils.QUOT:
            temp.append(cur)
            if not quot:
                quot = cur
            elif quot == cur:
                quot = ''
        elif cur == '@' and not quot:
            continue
        else:
            temp.append(cur)
        if n == length -1:
            if not cmd[0] and temp:
                cmd[0] = ''.join(temp)
                temp = []
                result.append(cmd)
                cmd = new_cmd()
            break
    return result

def pickup(node_tree, cmd_string):
    """docstring for pickupo
     node_tree #[['div', [7, 109], {}, [['div', [17, 89], {}, [['br', [32, 32], {}, []], ['img', [61, 61], {'src': '"aldskjf"'}, []], ['br', [67, 67], {}, []], ['a', [79, 80], {}, []]]], ['a', [103, 104], {}, []]]]]

    cmd_list #[['div', 1, {'class': '"sss:\'111\'"'}], ['div', 2, {'id': "'jjj'"}], ['a', 2, {}]]
    """
    cmd_list = path_parser(cmd_string)
    temp_1 = copy.copy(node_tree)
    temp_2 = []
    result = []
    n = 0
    cmd_count = len(cmd_list)-1

    while n <= cmd_count:
        temp_2 = []
        cmd = cmd_list[n]
        if cmd[1] == 3:
            while temp_1:
                node = temp_1.pop(0)
                if node[0] == cmd[0]:
                    if n == cmd_count:
                        result.append(node)
                    else:
                        temp_2.extend(node[3])
                if node[3]:
                    temp_1.extend(node[3])
        elif cmd[1] == 2:
            for node in temp_1:
                if cmd[0] == node[0]:
                    if n == cmd_count:
                        result.append(node)
                    else:
                        temp_2.extend(node[3])
        temp_1 = temp_2
        n += 1
    return result
