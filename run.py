from flaskblog import app

# 127.0.0.1:5000 is I.P. address and port for local host.
# I.P. can be replaced by string 'localhost', i.e. localhost:5000
if __name__ == "__main__":
    app.run(debug=True)
