from flask import Flask
from routes.main import main_bp

app = Flask(__name__)
app.secret_key = "supersecretkey" 
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
