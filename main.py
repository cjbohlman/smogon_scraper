# maybe interace with smogon damage calculator?

# py -m pip install flask
from flask import Flask, render_template

# py -m pip install flask_restful
from flask_restful import Resource, Api

from smogon_retriever import SMOGON_RETRIEVER

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return render_template('index.html')

class SMOGON_API(Resource):
    def get(self, generation, pokemon):
        data = SMOGON_RETRIEVER().get_data(pokemon, generation)
        return data

api.add_resource(SMOGON_API, '/pkmn/<generation>/<pokemon>')

# if __name__ == '__main__':
#     app.run(debug=False)

