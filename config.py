import os

class Config:
    '''
    Parent config class
    '''
   
    # Mail confugurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS=True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SUBJECT_PREFIX = 'Minute Pitcher!'
    SENDER_EMAIL = 'minutepitcher@gmail.com'


    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    



DEBUG = True


class TestConfig(Config):
    '''
    Test
    '''



class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''



config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig,
}