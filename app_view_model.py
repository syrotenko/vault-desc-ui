from logger import get_logger


class AppViewModel:
    def __init__(self):
        self.logger = get_logger()
        self.server = 'http://127.0.0.1:8200'
        self.connect_method = ConnectMethod.Token
        self.token = ''
        self.ldap_user = ''
        self.ldap_pass = ''

    def connect(self, **args):
        self.logger.info(f'Connect with params: \n{args}')
        self.server = args.get('server', None)
        self.connect_method = args.get('connect_method', None)
        self.token = args.get('token', None)
        self.ldap_user = args.get('ldap_user', None)
        self.ldap_pass = args.get('ldap_pass', None)


class ConnectMethod:
    Token = 'token'
    LDAP = 'ldap'
