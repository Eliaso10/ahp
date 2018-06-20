#!/usr/bin/env python3
import sys
import ahp 
import os.path


def main():
    criteria_file = input('what are is your criteria? ')
    top_n = int(input('choose top: '))
    assert os.path.isfile(criteria_file), "file does not exist"
    assert top_n > 0 , "you need to pick more then 0 people"
    criteria = ahp.read_criteria(criteria_file)
    weights, skills= ahp.get_weights(criteria)
    top_students = ahp.get_top_n_students('grades.json',top_n,weights,skills)
    print(top_students)

if __name__ == '__main__':
	main()