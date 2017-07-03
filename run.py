import init_app


if __name__ == "__main__":
    init_app.app.secret_key = "sooper_secret_key_dood"
    init_app.app.debug = True
    init_app.app.run()

