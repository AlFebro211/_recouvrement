import re
import os

def check_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.splitlines()
    stack = []
    
    # regex for django tags
    tag_re = re.compile(r'{%\s*(if|elif|else|endif|for|empty|endfor)\b')
    
    for i, line in enumerate(lines, 1):
        for match in tag_re.finditer(line):
            tag = match.group(1)
            if tag in ['if', 'for']:
                stack.append((tag, i))
            elif tag == 'endif':
                if not stack:
                    print(f"Error: unmatched endif at line {i}")
                elif stack[-1][0] == 'if':
                    stack.pop()
                else:
                    print(f"Error: endif at line {i} matches {stack[-1][0]} from line {stack[-1][1]}")
                    stack.pop()
            elif tag == 'endfor':
                if not stack:
                    print(f"Error: unmatched endfor at line {i}")
                elif stack[-1][0] == 'for':
                    stack.pop()
                else:
                    print(f"Error: endfor at line {i} matches {stack[-1][0]} from line {stack[-1][1]}")
                    stack.pop()
            elif tag in ['elif', 'else']:
                if not stack or stack[-1][0] != 'if':
                    print(f"Error: {tag} at line {i} without active if")
            elif tag == 'empty':
                if not stack or stack[-1][0] != 'for':
                    print(f"Error: empty at line {i} without active for")

    if stack:
        for tag, line in stack:
            print(f"Error: UNCLOSED {tag} from line {line}")
    else:
        print("All tags balanced!")

if __name__ == "__main__":
    check_tags(r'e:\recovrement_app\_recouvrement\recouvrement\app\templates\recouvrement\index_recouvrement.html')
