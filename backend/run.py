from app import create_app

app = create_app()

if __name__ == '__main__':
    # Running on port 5000 by default. 
    # Use debug=True for development, which auto-reloads on code changes.
    app.run(debug=True, port=5000)
