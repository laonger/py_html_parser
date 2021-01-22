#!/usr/bin/env pypy3

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

def cmd_2(node_tree, cmd):
    """docstring for cmd_1 /"""
    result = []
    if cmd[2]:
        key, value = list(cmd[2].items())[0]
    else:
        key = ''
        value = ''
    for node in node_tree:
        if node[0] == cmd[0]:
            if key:
                if node[2].get(key) == value:
                    result.append(node)
            else:
                result.append(node)
    return result

def cmd_3(node_tree, cmd):
    """docstring for cmd_1 //"""
    result = []
    if cmd[2]:
        key, value = list(cmd[2].items())[0]
    else:
        key = ''
        value = ''
    def f(result, node_tree, cmd, key, value):
        """docstring for f"""
        for node in node_tree:
            if node[0] == cmd[0]:
                if key:
                    if node[2].get(key) == value:
                        result.append(node)
                else:
                    result.append(node)
            if node[3]:
                f(result, node[3], cmd, key, value)
    f(result, node_tree, cmd, key, value)
    return result




def pickup(node_tree, cmd_string):
    """docstring for pickupo
     node_tree #[['div', [7, 109], {}, [['div', [17, 89], {}, [['br', [32, 32], {}, []], ['img', [61, 61], {'src': '"aldskjf"'}, []], ['br', [67, 67], {}, []], ['a', [79, 80], {}, []]]], ['a', [103, 104], {}, []]]]]

    cmd_list #[['div', 1, {'class': '"sss:\'111\'"'}], ['div', 2, {'id': "'jjj'"}], ['a', 2, {}]]
    """
    cmd_list = path_parser(cmd_string)
    f = node_list[0]
    pick = False
    cmd = cmd_list[0]
    if cmd[0] == f[0]:
        cmd = cmd_list[1]
        f = f[3][0]
        if cmd[0] == f[0]:
            pass
        else:
            f = f[3][1]
            if cmd[0] == f[0]:
                pass
            else:
                pass

    return node_list



def aaaa(node_tree, cmd_list, result=None, n=0, max_n=0):
    """docstring for a"""
    if result is None:
        result = []
    if not max_n:
        max_n = len(cmd_list)-1
    if n > max_n:
        result.extend(node_tree)
        return result
    cmd = cmd_list[n]
    for node in node_tree:
        if node[0] == cmd[0]:
            n += 1
            result.extend(aaaa(node[3], cmd_list, result, n, max_n))
        elif node[3]:
            result.extend(aaaa(node[3], cmd_list, result, n, max_n))
    return result












