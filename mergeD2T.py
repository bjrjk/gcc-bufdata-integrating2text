import re, ast

def readT(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def writeT(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

def compile(match):
    name = match.group(1)
    buf = ast.literal_eval(f"b'{match.group(2)}'")
    header = "__attribute__ ((aligned (1))) char\n"
    result = ""
    for i in range(0, len(buf), 4):
        fmt_content = ""
        flag = False
        for j in range(0, min(4, len(buf) - i)):
            if not flag:
                flag = True
            else:
                fmt_content += ', '
            fmt_content += f"{buf[i + j]}"
        fmt_content = f"{name}_{i}[] = " + "{" + fmt_content + "}"
        if i != 0:
            fmt_content += ','
        result = fmt_content + "\n" + result
    result = header + result + ';\n'
    result += f"char* {name} = {name}_0"
    return result

def merge(input_file, output_file):
    content = readT(input_file)
    pattern = re.compile(r'INLINE_DATA_GEN\([ ]*([a-zA-Z0-9_]+)[ ]*,[ ]*(.*)[ ]*\)', re.M)
    compiled_content = pattern.sub(compile, content)
    writeT(output_file, compiled_content)

def main():
    input_file = 'test/test.c'
    output_file = 'test/test_processed.c'
    merge(input_file, output_file)

if __name__ == '__main__':
    main()