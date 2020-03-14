
from test.support import testing_base as base
from util.environment import MasonEnvironment
from definitions import from_root
from util.yaml import parse_yaml
from configurations import Config

class TestConfiguration:

    def before(self, config: str):
        base.set_log_level("fatal")
        config_home = from_root(config)
        env = MasonEnvironment(config_home=config_home)
        config_doc = parse_yaml(env.config_home)
        conf = Config(env, config_doc)
        return conf

    def empty_config(self):
        return {}

    def test_configuration_path_dne(self):
        conf = self.before("path_dne")
        assert(conf.config == {})

    def test_configuration_invalid_yaml(self):
        conf = self.before("/test/support/invalid_yaml.yaml")
        assert(conf.config == {})

    def test_configuration_invalid_yaml_2(self):
        conf = self.before("/test/support/invalid_yaml_2.yaml")
        assert(conf.config == {})

    def test_configuration_invalid_config(self):
        conf = self.before("/test/support/test_bad_config.yaml")
        assert(conf.config == {})

    def test_configuration_valid(self):
        conf = self.before("/test/support/valid_config_1.yaml")
        expects = {'execution': {'client_name': '', 'configuration': {}},
             'metastore': {'client_name': '', 'configuration': {}},
             'scheduler': {'client_name': '', 'configuration': {}},
             'storage': {'client_name': 's3',
             'configuration': {'test_param_1': 'test', 'test_param_2': 'test'}}
       }
        assert(conf.config == expects)
