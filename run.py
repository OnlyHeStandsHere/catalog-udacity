import init_app


if __name__ == "__main__":
    init_app.app.secret_key = "sooper_secret_key_dood"
    init_app.app.debug = True
    #init_app.app.run(host='0.0.0.0', port=5000)
    init_app.app.run(port=5000)
