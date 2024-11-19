from flask import Flask
from views.user_view import user
from views.Task_view import task
app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(task)
@app.route('/', methods=['GET'])
def home():
    return "<h1>HOME 52</h1>"

# client = MongoClient("mongodb+srv://renancavalcanti:IvzIJZklg5PMONvm@cluster0.rfbzg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client['LS3FALL2024']
# users_collection = db['Users']

if __name__ == '__main__':
    app.run()
