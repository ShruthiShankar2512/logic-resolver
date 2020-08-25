import copy
import itertools

#Reading contents from the file. Returns a list of all the lines as strings
def readFile(fileName) -> list:
    file = open(fileName,"r")
    lines = file.readlines()
    lines = [i.strip('\n') for i in lines]
    file.close()
    return lines



#Understanding file contents

#Input: array of file elements
# Function takes all the file elements listed as strings,
#     processes and stores the required information into a dictionary as directed in the problem statement
#Output: Dictionary containing all the reuired information

def getInfo(lines) -> dict:
    details = {}
    details["num_of_queries"] = int(lines[0])
    details["query_list"] = []
    for i in range(1,details["num_of_queries"]+1):
        details["query_list"].append(lines[i])
    details["kb"] = []
    for i in range(details["num_of_queries"]+2,len(lines)):
        details["kb"].append(lines[i])
    details['kb_size'] = len(details['kb'])
    return details


lines = readFile("input.txt")
details = getInfo(lines)


class Variable:
    def __init__(self, var):
        var = var.replace(" ","")
        self.name = var

    def print_element(self):
        print("var", self.name)

class Constant:
    def __init__(self, const):
        const = const.replace(" ","")
        self.name = const

    def print_element(self):
        print("const", self.name)

#Takes in a string and processes it. Stores the predicate name, the arument list and whether the literal has a negation.
class Literal:
    def __init__(self, string):
        self.predicate = None
        self.arguments = []
        self.negation = False
        self.process_literal(string)


    #This function processes/parses the literal
    def process_literal(self, string):
        #Check for negation
        if '~' in string:
            self.negation = True
            string.replace('~','')
        #Split at '(', and store the first part as the predicate name

        split_res = string.split('(')
        self.predicate = string.split('(')[0]
        self.predicate = self.predicate.replace(" ","")
        #Takes the second part, remove the last ')', split it and separate using the ',', and form the argument list.
        arg_set = split_res[1].replace(')',"")
        args_list = arg_set.split(',')
        #Check whether each argument is a var or a const. Constant always begins with an Uppercase character.
        #Instantiate the object accordingly, and append it into the arguments list.
        for element in args_list:
            if element[0].islower():
                ele = Variable(element)
                self.arguments.append(ele)
            else:
                ele = Constant(element)
                self.arguments.append(ele)



    def print_lit(self):
        print("negation", self.negation)
        print("predicate name", self.predicate)
        print("argument list")
        for i in self.arguments:
            i.print_element()

    #print the literal.
    def print_literal(self):
        if self.negation:
            #print('~', end = " ")
            pass
        print(self.predicate, end = "")
        print("(", end = "")
        for i in range(len(self.arguments)):
            print(self.arguments[i].name, end = "")
            if i!= len(self.arguments) - 1:
                print(",", end = "")
        print(")", end = "")

    def get_constants(self):
        constants = []
        all_arguments = self.arguments
        #go through all the literals. Check if the arguments have a Constant object. If it does, add it to the list.
        for i in all_arguments:
            flag = False
            if isinstance(i, Constant):
                for j in constants:
                    if i.name == j.name:
                        flag = True
                if flag == False:
                    constants.append(i)

        if len(constants) == 0:
            constants = None
        return constants


    def is_fact(self):
        fact_bool = True
        for i in self.arguments:
            #print(i)
            if isinstance(i, Variable):
                fact_bool = False
                #print("not fact")
                break
        return fact_bool



    def get_variables(self):
        variables = []
        all_arguments = self.arguments
        #go through all the literals. Check if the arguments have a Variable object. If it does, add it to the list.
        #use the flag to not add the same variables multiple times.
        for i in all_arguments:
            flag = False
            if isinstance(i, Variable):
                for j in variables:
                    if i.name == j.name:
                        flag = True

                if flag == False:
                    variables.append(i)

        if len(variables) == 0:
            variables = None

        return variables


    def replace_variable(self, var, const):
        literal_copy = copy.deepcopy(self)
        #Check if a literal contains a variable
        for j in literal_copy.arguments:
            if isinstance(j, Variable):
                j.name = j.name.replace(" ","")
                var.name = var.name.replace(" ","")
                #if it matches the required variable, replace it with the constant object from the argument
                if j.name == var.name:
                    index = literal_copy.arguments.index(j)
                    literal_copy.arguments[index] = const
        return literal_copy





class Sentence:
    #Takes a string and processes it.
    def __init__(self, string):
        self.implication = False
        #self.conjunction = False
        self.premise = None
        self.conclusion = None

        #sent will always be a list.
        #if its len is 1, its a literal
        #if its len is 2, its an implication,
        #    with the first element being a list of literals in the premise, separated by '&',
        #    and the second element being a literal in the conclusion.
        self.sent = self.process_sentence(string)


    def process_conjunction(self, string):
        string = string.replace(' ','')
        #split it at '&'
        conjunction_split_list = string.split('&')
        #if it's multiple literals, make a list, and instantiate each of them and append. Finally return the list of conjunctions
        if len(conjunction_split_list) > 1:
            #self.conjunction = True
            conjunction_args = []
            for lit in conjunction_split_list:
                conjunction_args.append(Literal(lit))
            return conjunction_args
        #else just return a list containing one literal.
        else:
            return [Literal(string)]


    def process_sentence(self, string):
        string = string.replace(' ','')
        #split at =>
        implication_split_list = string.split('=>')
        #if it is an implication
        if len(implication_split_list) > 1:
            self.implication = True
            self.premise = self.process_conjunction(implication_split_list[0])
            self.conclusion = Literal(implication_split_list[1])
            #print(self.premise)
            #print(self.conclusion)
            #form -> [ [premise], conclusion ]
            return [self.premise, self.conclusion]
        #if it is a conjunction of literals with no implication
        elif '&' in string and '=>' not in string:
            return self.process_conjunction(string)
        #if it is just one literal
        else:
            return [Literal(string)]

    def print_sentence(self):
        if self.implication:
            for i in range(len(self.premise)):
                self.premise[i].print_literal()
                if i < len(self.premise)-1:
                    print(" & ", end = "")
            print(" => ", end = "")
            (self.conclusion).print_literal()
        else:
            for i in self.sent:
                i.print_literal()
        print("\n")


    def get_literals(self):
        #get all the literals
        if self.implication:
            list_of_literals = []
            for i in self.sent[0]:
                list_of_literals.append(i)
            list_of_literals.append(self.sent[1])
        else:
            list_of_literals = self.sent
        return list_of_literals


    def get_constants(self):
        constants = []

        #get all the literals
        list_of_literals = self.get_literals()

        #get all the arguments
        all_arguments = []
        for i in list_of_literals:
            all_arguments.append(i.arguments)
        #flatten the argument list
        all_arguments = [item for sublist in all_arguments for item in sublist]

        #go through all the literals. Check if the arguments have a Constant object. If it does, add it to the list.
        for i in all_arguments:
            flag = False
            if isinstance(i, Constant):
                for j in constants:
                    if i.name == j.name:
                        flag = True
                if flag == False:
                    constants.append(i)

        if len(constants) == 0:
            constants = None
        return constants

    def get_variables(self):
        variables = []

        #get all the literals
        list_of_literals = self.get_literals()

        #get all the arguments
        all_arguments = []
        for i in list_of_literals:
            all_arguments.append(i.arguments)
        #flatten the argument list.
        all_arguments = [item for sublist in all_arguments for item in sublist]

        #go through all the literals. Check if the arguments have a Variable object. If it does, add it to the list.
        #use the flag to not add the same variables multiple times.
        for i in all_arguments:
            flag = False
            if isinstance(i, Variable):
                for j in variables:
                    if i.name == j.name:
                        flag = True

                if flag == False:
                    variables.append(i)

        if len(variables) == 0:
            variables = {}

        return variables


    def replace_variable(self, var, const):
        #get all the literals
        sentence_copy = copy.deepcopy(self)
        list_of_literals = sentence_copy.get_literals()
        #Check if a literal contains a variable
        for lit in list_of_literals:
            for j in lit.arguments:
                if isinstance(j, Variable):
                    j.name = j.name.replace(" ","")
                    var.name = var.name.replace(" ","")
                    #if it matches the required variable, replace it with the constant object from the argument
                    if j.name == var.name:
                        index = lit.arguments.index(j)
                        lit.arguments[index] = (const)
        return sentence_copy


class KnowledgeBase:
    def __init__(self, list_of_sentences):
        self.sentences = []
        #all the literals in the kb
        self.literals = []
        #all the facts in the kb i.e. literals with constant arguments.
        self.facts = []
        #all non-facts.
        rules = []
        self.raw_sentences = list_of_sentences

        for sent in list_of_sentences:
            self.tell(sent)



    def tell(self,sentence = None):
        if isinstance(sentence, Literal):
            if sentence not in kb.literals:
                #print("appending new conclusion\n\n")
                #kb.sentences.append(sentence)
                kb.literals.append(sentence)
                kb.facts.append(sentence)
                fc_ask(kb, sentence)
        else:
            sentence_obj = Sentence(sentence)
            self.sentences.append(sentence_obj)
            list_of_literals = sentence_obj.get_literals()

            for i in list_of_literals:
                if all(isinstance(x, Constant) for x in i.arguments):
                    self.facts.append(i)
                self.literals.append(i)
        #TODO
        #include fc and add those queries too.

    def ask(self, query):
        assert isinstance(query, Literal)

        #go through all the facts/literals in the kb. If the query literal is in it, then return True.
        for lit in self.facts:
            in_kb = True
            if query.predicate == lit.predicate:
                if query.negation == lit.negation:
                    if len(query.arguments) == len(lit.arguments):
                        for i in range(len(query.arguments)):
                            if query.arguments[i].name != lit.arguments[i].name:
                                #print("args dont match ", query.arguments[i].name, lit.arguments[i].name)
                                in_kb = False
                    else:
                        #print("arg lengths dont match")
                        in_kb = False
                else:
                    #print("negation doesnt match")
                    in_kb = False
            else:
                #print("predicate doesnt match")
                in_kb = False
            if(in_kb):
                #print("all match")
                return True
        return False


    def print_kb(self):
        for i in self.sentences:
            i.print_sentence()
        print("facts")
        print(len(self.facts))
        print(self.facts)
        for i in self.facts:
            i.print_literal()
        print("literals")
        print(len(self.literals))
        print(self.literals)
        for i in self.literals:
            i.print_literal()



def occurs_check(var, term, sub):
    assert isinstance(var, Variable)
    if var == term:
        return True
    elif isinstance(term, Variable) and term.name in sub:
         return occurs_check(var, sub[term.name], sub)
    elif isinstance(term, Literal):
        return any(occurs_check(var, arg, sub) for arg in term.arguments)
    else:
        return False


def unify_var(var, x, sub):
    assert isinstance(var, Variable)
    if var.name in sub:
        return unify(sub[var.name], x, sub)
    elif isinstance(x, Variable) and x.name in sub:
        return unify(var, sub[x.name], sub)

    elif occurs_check(var, x, sub):
        #print("Occurs Check", var, x, sub)
        return None
    else:
        return {**sub, var: x}



def unify(sent1, sent2, sub):

    if sub is None:
        #print("Sub is none")
        return None
    elif sent1 == sent2:
        #print("both are equal")
        return sub
    elif isinstance(sent1, Variable):
        #print("sent1 is var")
        return unify_var(sent1, sent2, sub)
    elif isinstance(sent2, Variable):
        #print("sent2 is var")
        return unify_var(sent2, sent1, sub)
    #if they're both constants, check if they're the same.
    elif isinstance(sent1, Constant) and isinstance(sent2, Constant):
        #print("both are consts")
        if sent1.name == sent2.name:
            return sub
        else:
            #print("not same constant so None")
            return None
    elif isinstance(sent1, Literal) and isinstance(sent2, Literal):
        #print("both are literal")
        if sent1.predicate != sent2.predicate or len(sent1.arguments) != len(sent2.arguments):
            #print("Argument not matching so none")
            return None
        else:
            #print("unify lit args")
            for i in range(len(sent1.arguments)):
                sub = unify(sent1.arguments[i], sent2.arguments[i], sub)
            return sub
    else:
        #print("final none")
        #print(sent1, sent2)
        return None





def subst(s, sent):
    sentence_copy = copy.deepcopy(sent)
    for var in s:
        sentence_copy = sentence_copy.replace_variable(var,s[var])
    return sentence_copy



def is_valid_sub(literal, sub_literal):
    variables = set([i.name for i in literal.arguments])
    constants = set([i.name for i in sub_literal.arguments])
    if len(variables) != len(constants):
        return False
    return True



def is_valid_prem_sub(prem, sub_prem):
    variables = [prem[i].get_variables() for i in range(len(prem))]
    variables = set([item.name for sublist in variables for item in sublist])
    constants_in_prem = [prem[i].get_constants() for i in range(len(prem)) if prem[i].get_constants() is not None]
    constants_in_prem = set([item.name for sublist in constants_in_prem for item in sublist])
    constants = [sub_prem[i].get_constants() for i in range(len(sub_prem))]
    constants = set([item.name for sublist in constants for item in sublist])
    constants = constants.difference(constants_in_prem)
    if len(variables) != len(constants):
        return False
    return True




def substitute_premise(s, prem):
    prem_copy = copy.deepcopy(prem)
    list_prem = []
    for i in prem_copy:
        for var in s:
            before_sub = i
            i = before_sub.replace_variable(var, s[var])
            if i.is_fact():
                list_prem.append(i)
            else:
                pass
    if not is_valid_prem_sub(prem, list_prem):
        list_prem = []

    return list_prem



def is_valid_sub_dict(s, len_of_query_vars):
    name_dict = {}
    valid = True
    variables = [i for i in s.keys()]

    variables = [i.name for i in variables]
    variables = set(variables)
    constants = set([i.name for i in s.values()])

    if len(variables)!=len(constants):

        return False
    for key in s:
        if key.name not in name_dict:
            name_dict[key.name] = []
            name_dict[key.name].append(s[key].name)
        else:
            name_dict[key.name].append(s[key].name)

            if len(set(name_dict[key.name])) > 1:
                #print("MULTIPLE VALUES FOR VARIABLE :",key.name, "",name_dict[key.name])
                return False
    return True




#Used the method of forward chaining to handle inference from the knowledge base.
#FC takes definite clause as input hence changing the format of the input was not required.
def fc_ask(kb, alpha):
    kb_consts = list({c for clause in kb.facts for c in clause.get_constants()})

    constants = [i.name for i in kb_consts]
    constants = list(set(constants))

    def temp_subst(p):
        query_vars = list({v for clause in p for v in clause.get_variables()})


        final_dict= {}
        query_vars = list(set([i.name for i in query_vars]))
        for assignment_list in itertools.product(constants, repeat=len(query_vars)):
            theta = {Variable(x): Constant(y) for x, y in zip(query_vars, assignment_list)}

            if is_valid_sub_dict(theta, len(query_vars)):
                yield theta

    # check if we can answer without new inferences
    for q in kb.literals:
        #print("check if we can answer without new inferences")
        phi = unify(q, alpha, {})
        if phi is not None:
            yield phi

    #print("cannot answer without new inferences")
    while True:
        kb_change = False
        new = []
        for rule in kb.sentences:
            if rule.implication:
                p, q = rule.premise, rule.conclusion
                for theta in temp_subst(p):
                    substituted_premise = substitute_premise(theta, p)
                    if not substituted_premise:
                        #print("Not a valid substitution! \n\n\n")
                        continue

                    for literal1 in substituted_premise:
                        in_kb = kb.ask(literal1)
                        if not in_kb:
                            break

                    if in_kb:
                        #print("substitution of p is a subset of literals")
                        q_ = subst(theta, q)
                        if not kb.ask(q_):
                            #print("new conc not in kb")
                            kb.literals.append(q_)
                            kb.facts.append(q_)
                            kb_change = True
        if not kb_change:
            break
    for clause in new:
        kb.tell(clause)
    if kb.ask(alpha):
        #print("TRUE")
        return True
    else:
        #fc_ask(kb,alpha)
        return False


def main():
	kb = KnowledgeBase(details['kb'])
	final_list = []
	for query in details['query_list']:
	    ans = fc_ask(kb, Literal(query))
	    for i in ans:
	    	pass
	    query_in_kb = kb.ask(Literal(query))

	    if query_in_kb:
	        final_list.append("TRUE")
	    else:
	        final_list.append("FALSE")

	fp = open("output.txt", "w")

	for i in final_list:
		fp.write(i)
		fp.write("\n")

	fp.close


if __name__ == "__main__":
	main()
