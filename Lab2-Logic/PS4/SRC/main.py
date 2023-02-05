''' Read data from the input file '''
# Input: string filename
# Output: alpha and list of KB
def read_file(filename):
    KB, alpha = [], []
    with open(filename, 'r') as file:
        alpha = [file.readline()[:-1].rstrip().split(' OR ')]
        num_of_clauses = int(file.readline())
        for i in range(num_of_clauses):
            line = file.readline().rstrip().split(' OR ')
            clause = []
            for sub in line:
                clause.append(sub.replace('\n', ''))
            KB.append(clause)
    file.close()
    return KB, alpha


''' Propositional Logic Resolution function'''
# Input: KB, alpha
# Output: solution (True/ False), new_clauses
def pl_resolution(KB, alpha):
    clauses = copy_list(KB)
    neg_alpha = negative_clause(alpha)
    for i in range(len(neg_alpha)):
        clauses.append(neg_alpha[i])
    new_clauses = []
    while True:
        new_clauses.append([])

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvents = resolve(clauses[i], clauses[j])
                if [] in resolvents:
                    new_clauses[-1].append([])
                    return True, new_clauses

                for resolvent in resolvents:
                    if is_valid(resolvent):
                        break
                    if resolvent not in clauses and resolvent not in new_clauses[-1]:
                        new_clauses[-1].append(resolvent)

        if len(new_clauses[-1]) == 0:
            return False, new_clauses
        clauses += new_clauses[-1]


''' Write data to the output file '''
# Input: string filename, KB, alpha
# Output: a file with the solution and the clauses was created by KB and negative alpha
def write_file(filename, KB, alpha):
    solution, new_clauses = pl_resolution(KB, alpha)
    with open(filename, 'w') as file:
        for clauses in new_clauses:
            file.write(str(len(clauses)) + '\n')
            for clause in clauses:
                file.write(parse_string(clause) + '\n')
        if solution == True:
            file.write('YES') 
        else: 
            file.write('NO')
    file.close()


''' Copy source list to destination list '''
# Input: source list
# Output: a copy list from source list
def copy_list(src):
    dest = []
    for i in range(len(src)):
        dest.append(src[i])
    return dest


''' Negation of a literal '''
# Input: literal
# Output: a negative literal
# Example: '-A' --> 'A'  |  'A' --> '-A'
def negative_literal(literal: str):
    if literal[0] == '-':
        return literal[1]
    return '-' + literal


''' Whether a clause is empty or not '''
# Input: clause
# Output: a clause is NOT empty
def is_empty(clause):
    if len(clause) == 0:
        return True
    else:
        return False


''' Whether 2 literals are complementary '''
# Input: 2 literals
# Output: True if they are complementary, False if they are not
# Example: -A and A are complementary
def is_complementary(first_literal: str, second_literal: str):
    if len(first_literal) != len(second_literal) and first_literal[-1] == second_literal[-1]:
        return True
    else:
        return False


''' Whether a clause is valid '''
# Input: clause
# Output: True if they are valid, False if they are NOT valid
def is_valid(clause):
    for i in range(len(clause) - 1):
        if is_complementary(clause[i], clause[i + 1]):
            return True
    else:
        return False


''' Remove duplicates and sorted literals from clause '''
# Input: clause
# Output: a new clause with unduplicated and sorted literals
# Example: ['A' , '-B' , '-A', 'B'] --> ['-A', 'B']
def removed_duplicates_and_sorted(clause: list):
    new_clause = []
    for i in range(len(clause)):
        if clause[i] not in new_clause:
            new_clause.append(clause[i])
    new_clause = sorted(new_clause, key=lambda x: x[-1])
    return new_clause


''' Parse clause to string '''
# Input: clause
# Output: a clause with string format
# Example: ['A', 'B'] --> 'A OR B'
def parse_string(clause: list):
    if (is_empty(clause)):
        return '{}'
    result = ''
    for i in range(len(clause) - 1):
        result += str(clause[i]) + ' OR '
    else:
        result += str(clause[-1])
    return result


''' Negation of a clause '''
# Input: clause
# Output: a negative clause
# Example: ['-A', 'B'] --> ['A', '-B']
def negative_clause(clause: list):
    neg_clause = []
    for literal in clause[0]:
        literal = negative_literal(literal)
        neg_clause.append(literal)
    neg_clause = list(map(lambda x: [x], neg_clause))
    return neg_clause


''' Resolve 2 clause '''
# Input: 2 clause
# Output: 1 clause is resolved
def resolve(first_clause: list, second_clause: list):
    resolvents = []
    for i in range(len(first_clause)):
        for j in range(len(second_clause)):
            if is_complementary(first_clause[i], second_clause[j]):
                resolvent = first_clause[:i] + first_clause[i + 1:] + second_clause[:j] + second_clause[j + 1:]
                resolvents.append(removed_duplicates_and_sorted(resolvent))
    return resolvents


''' Main function to read file, store data and write results to output file'''
if __name__ == '__main__':
    # Number of testcase input files
    NUM_OF_FILES = 5
    for i in range(NUM_OF_FILES):
        KB, alpha = [], []
        KB, alpha = read_file('../SRC/INPUT/input%s.txt' % str(i))
        write_file('../SRC/OUTPUT/output%s.txt' % str(i), KB, alpha)