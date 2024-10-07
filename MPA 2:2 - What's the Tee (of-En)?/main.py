## identify one counts

## classify into
## linear statements
## quadratic statements
## cubic statments
#-----------------------------------#

import re
#public variables
lines = []


def inputToArray():
    inp = int(input())
    for i in range(inp):
        lines.append(input())

def lineIdentifier(line):
    variable_pattern = r'\b[_a-zA-Z][_a-zA-Z0-9]*\b'
    assignment_pattern = rf'{variable_pattern}\s*=\s*(.*?)\s*;'
    
    # Define line patterns
    line_patterns = {
        'declaration': r'(int|char|bool|long|string)\s+[a-zA-Z_]\w*',    # lazy, lacking
        'assignment': assignment_pattern,
        'braced_if': r'if\s*\((.*?)\)\s*{',                              # lazy, greedy, lacking
        'if': r'if\((.*?)\)'                                             # lazy, greedy, lacking
    }

    for type, pattern in line_patterns.items():
        if re.match(pattern, line):
            return type
    
    return 'undefined.'

def linearHandler():
    pass

def quadraticHandler():
    pass

def cubicHandler():
    pass


inputToArray()

for line in lines:
    print(lineIdentifier(line))

