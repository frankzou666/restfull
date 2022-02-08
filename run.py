


from restfull import app
import logging

def main():
    """

    :return:
    """
    logging.info('app start...')
    app.run(host=app.config['LISTENHOST'])


if __name__ == '__main__':
    main()