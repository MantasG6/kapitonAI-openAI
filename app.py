from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, ObjectType
from api.queries import getTripPlan_resolver

query = ObjectType("Query")
query.set_field("getTripPlan", getTripPlan_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query
)

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(port=5000, debug=True)