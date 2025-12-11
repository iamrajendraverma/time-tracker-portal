from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run on a different port than the API (5001)
    app.run(host='0.0.0.0', port=5002, debug=True)
