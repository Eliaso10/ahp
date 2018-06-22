import ahpmod
import util

def get_best_students(event, context):
    criteria = event['criteria']
    top_n = event['number']
    weights, skills= ahpmod.get_weights(criteria)
    top_students = ahpmod.get_top_n_students(event['grades'],top_n,weights,skills)
    return util.jsonify(top_students)