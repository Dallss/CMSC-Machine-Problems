## identify one counts

## classify into
## linear statements
## quadratic statements
## cubic statments
#-----------------------------------#

# !!! OPTIMIZE REGEX !!!

import re
#public variables
lines = []
variable_pattern = r'\b[_a-zA-Z][_a-zA-Z0-9]*\b'
integer_pattern = r'[-+]?\b\d+\b'
value_pattern = rf'({integer_pattern}|{variable_pattern})'
operator_pattern = r'[+\-*/%]'
assignment_pattern = rf'{variable_pattern}\s*=\s*(.*?)\s*[,;]'
operation_pattern = rf'\s*{value_pattern}\s*{operator_pattern}\s*{value_pattern}\s*'

#ran into problem with case 1 - try tokenizing 

# x = 10 - -10;

linear_total = 0

state = 'linear'

def inputToArray():
    inp = int(input())
    for i in range(inp):
        lines.append(input())

def lineIdentifier(line):    
    # Define line patterns
    line_patterns = {
        'declaration': r'(int|char|bool|long|string)\s+[a-zA-Z_]\w*',    # lazy, lacking
        'assignment': assignment_pattern,
        'braced_if': r'if\s*\((.*?)\)\s*{',                              # lazy, greedy, lacking
        'if': r'if\((.*?)\)',                                            # lazy, greedy, lacking
        'io': r'(cin|cout)(.*?)'                                         # lazy, greedy, lacking
    }

    for type, pattern in line_patterns.items():
        if re.match(pattern, line):
            return type
    
    return 'undefined.'

def lineCounter(line):

    line_type = lineIdentifier(line)
    if line_type == 'declaration':
        matches = re.findall(assignment_pattern, line)
        print('CONSOLE: returned: '+str(len(matches)))
        return len(matches)
    
    if line_type == 'io':                                     # verify
        return 1

    if line_type == 'assignment':
        operators = re.findall(operation_pattern,line)
        print('CONSOLE: returned: '+str(1+len(operators)))
        return 1 + len(operators)

    else:
        return -999
def linearHandler(line):
    global linear_total
    linear_total += lineCounter(line)

    

def quadraticHandler():
    pass

def cubicHandler():
    pass


inputToArray()

for line in lines:
    if state == 'linear':
        linearHandler(line)

print('T(n) = ' + str(linear_total))

