from visualization import create_dashboard

if __name__ == '__main__':
    app = create_dashboard()
    app.run_server(debug=True)
