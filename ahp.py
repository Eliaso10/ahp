import json

#needed this dictionary for negative numbers of the pariwise comparison matrix
pairwise_diff = {0:1, -1:1/2, -2:1/3, -3:1/4, -4:1/5, -5:1/6, -6:1/7, -7 :1/8, -8:1/9}

#reading in the data
def read_criteria(file):
    with open(file) as f:
        data = json.load(f)
    return data

#this function needed to reformat the grades json so Im able to reuse some of the methods/functions
def read_grades(json_file,list_of_skills):
    result_matrix = make_matrix(len(list_of_skills)) 
    with open(json_file) as f:
        data = json.load(f)
        for person, scores in data.items():
            if set(list_of_skills.values()) & scores.keys():
                for i in range(0, len(list_of_skills)):
                    skill = list_of_skills[i]
                    if skill in scores.keys():
                        n = bucketize(scores[skill])
                        result_matrix[i][person] = n
                    else:
                        result_matrix[i][person] = 0
    return result_matrix 


#main function in this module, it makes calls to other helper functions
def get_top_n_students(grades, top_n, weights, skills):
    grds , names = get_scores(grades, skills)
    score_dict = add_scores(combine_wighted_scores(grds,weights,skills))
    sorted_scores = sort_scores(score_dict)
    top = pick_top_n(names,sorted_scores,top_n)
    return top

#this functions makes a pairwise comparison and returns the weights/scores and the objective/names
def get_weights(att_dict):
    '''it takes in a dictionary and returns the weights in a dictionary'''
    length = 0 
    att_names = {}
    att_val = {}
    for k, v in att_dict.items():
        att_names[length] = k
        att_val[length] = v
        length +=1
    matrix = make_matrix(length)
    pairwiseMatrix = make_pairwise(matrix, att_val)
    added_columns = add_across(pairwiseMatrix, length, 'column')
    divided_matrix = divide_matrix(pairwiseMatrix, added_columns, length)
    weights = add_across(divided_matrix, length, 'row')
    return weights, att_names

#classifies the scores into the given buckets 
def get_scores(grades, skills):
    bucket_grades = read_grades(grades, skills)
    names = []
    grds = make_matrix(len(skills))
    i=0
    for g in bucket_grades.values():
        grds[i], names = get_weights(g)
        i+=1
    return grds, names

def bucketize(n):
    if n < 60:
        return 0
    elif n < 65 :
        return 1
    elif n < 70:
        return 2
    elif n < 75:
        return 3
    elif n < 80:
        return 4
    elif n < 85:
        return 5
    elif n < 90:
        return 6
    elif n < 95:
        return 7
    else:
        return 8


def make_matrix(length):
    objMatrix = {} #fromkeys(range(0,length),{})
    for i in range(0, length):
        objMatrix[i] = {}
    return objMatrix


def make_pairwise(matrix, attr):
    ma = matrix
    length = len(attr)
    for i in range(0, length):
        for j in range(0, length):
            col = attr[j]
            row = attr[i]
            if j not in ma[i]:
                n = row-col + 1.0
                if n <= 0:
                    ma[i][j] = pairwise_diff[n]
                else:
                    ma[i][j] = n
            if i not in ma[j]:
                n = row-col + 1.0
                if n <= 0:
                    pairwise_diff[n]
                else: 
                    ma[j][i] = 1/n
    return ma


def add_across(matrix, length, direction):
    added_axis = {}.fromkeys((range(0,length)),0)
    for i in range(0, length):
        for j in  range(0, length):
            if direction == 'row':
                added_axis[i] += matrix[i][j]
            elif direction =='column':
                added_axis[i] += matrix[j][i]
        if direction == 'row':
            added_axis[i] = added_axis[i]/length
    return added_axis


def divide_matrix(matrix, vector, length):
    m = matrix
    col_sum = vector
    for i in range(0, length):
        for j in  range(0, length):
            denominator = col_sum[j]
            m[i][j] = m[i][j]/denominator
    return m 


def combine_wighted_scores(scores_matrix,weights,skills): 
    row_len = len(scores_matrix[0])
    col_len = len(scores_matrix)
    weighted_matrix = make_matrix(row_len)
    for i in range(0, row_len):
        for j in range(0, col_len):
            weighted_matrix[i][j] = scores_matrix[j][i] * weights[j]
    return weighted_matrix


#normalize, apply weights, and sort scores
def add_scores(matrix_of_scores):
    row_len= len(matrix_of_scores[0])
    col_len= len(matrix_of_scores)
    added_axis = {}.fromkeys((range(0,col_len)),0)
    for i in range(0, col_len):
        for j in  range(0, row_len):
            added_axis[i] += matrix_of_scores[i][j]
    return added_axis


def sort_scores(score_dict):
    sorted_array = sorted(score_dict, key=score_dict.__getitem__,  reverse=True)
    return sorted_array


def pick_top_n(student_names, index_list, n):
    result = []
    for i in range(0,n):
        index= index_list[i]
        result.append(student_names[index])
    return result 