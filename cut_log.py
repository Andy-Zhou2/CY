CUT = 10000

with open('main.log') as f:
    lines = f.readlines()

# with open(f'last {CUT} lines.log', 'w') as f:
#     f.writelines(lines[-CUT:])

for line_count in range(len(lines)):
    if 'someone survived!' in lines[line_count]:
        print(f'Found survivor at line {line_count}')
        print(lines[line_count-100:line_count+100])
