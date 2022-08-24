from logger import get_logger
from v_node import VNode


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

    def get_first_node(self):
        # TODO: only for debug. Should be implemented in another way
        secret = VNode(parent=None, name='secret')
        d1 = VNode(parent=secret, name='d1')
        d3 = VNode(parent=secret, name='d3')
        secret.children = [d1, d3]
        return secret

    def get_children(self, node):
        # TODO: only for debug. Should be replaced with implementation of getting data from vault
        secret = self._get_whole_tree()
        full_tree_node = secret.get_node(node.get_full_path())
        found_children = full_tree_node.children
        for found_child in found_children:
            found_child.children = []
            found_child.kv = {}
        return found_children

    def _get_whole_tree(self):
        # TODO: only for debug. Should be removed
        secret = VNode(parent=None, name='secret')
        d1 = VNode(parent=secret, name='d1')
        d3 = VNode(parent=secret, name='d3')
        secret.children = [d1, d3]
        d11 = VNode(parent=d1, name='d11', kv={"google": "google_pass",
                                               "keplr": "keplr_pass"})
        d1.children = [d11]
        d31 = VNode(parent=d3, name='d31', kv={"github": "github_pass",
                                               "github_token": "github_token_pass",
                                               "github_user": "github_user_pass",
                                               "github_cred": "github_cred_pass"})
        d33 = VNode(parent=d3, name='d33', kv={"mono": "mono_pass",
                                               "privat": "privat_pass",
                                               "ukrsib": "ukrsib_pass"})
        d331 = VNode(parent=d33, name='d331', kv={"reddit": "reddit_pass",
                                                  "twitter": "twitter_pass"})
        d33.children = [d331]
        d34 = VNode(parent=d3, name='d34', kv={"spotify": "spotify_pass"})
        d3.children = [d31, d33, d34]
        return secret

    def get_node_data(self, node_path):
        # TODO: only for debug. Should be replaced with implementation of getting data from vault
        secret = self._get_whole_tree()
        node = secret.get_node(node_path)
        return node.kv

class ConnectMethod:
    Token = 'token'
    LDAP = 'ldap'
