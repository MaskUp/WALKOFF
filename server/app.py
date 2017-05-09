import os, logging

from jinja2 import Environment, FileSystemLoader
from core import helpers
from core.config import paths
import connexion
from gevent import monkey
from flask_security.utils import encrypt_password
from flask import Blueprint, g
monkey.patch_all()

logger = logging.getLogger(__name__)


#app_page = Blueprint('appPage', 'apps', template_folder=os.path.abspath('apps'), static_folder='static')


def read_and_indent(filename, indent):
    indent = '  '*indent
    with open(filename, 'r') as file_open:
        return ['{0}{1}'.format(indent, line) for line in file_open]


def compose_yamls():
    yaml_files = os.listdir(paths.swagger_apis)
    yaml_file_lookup = {}
    for api_yaml_file in yaml_files:
        with open(os.path.join(paths.swagger_apis, api_yaml_file), 'r') as yaml_file:
            yaml_file_lookup['./{0}'.format(api_yaml_file)] = yaml_file.read()
    with open(os.path.join(paths.swagger_apis, 'api.yaml'), 'r') as api_yaml:
        final_yaml = []
        for line in api_yaml:
            if line.lstrip().startswith('$ref:'):
                split_line = line.split('$ref:')
                reference = split_line[1].strip()
                indentation = split_line[0].count('  ')
                if reference in yaml_file_lookup:
                    final_yaml.extend(read_and_indent(os.path.join(paths.swagger_apis, reference), indentation))
                    final_yaml.append('\n')
                else:
                    logger.error('Could not find referenced YAML file {0}'.format(reference))
            else:
                final_yaml.append(line)
    with open(os.path.join(paths.swagger_apis, 'composed_api.yaml'), 'w') as composed_yaml:
        composed_yaml.writelines(final_yaml)


def create_app():
    connexion_app = connexion.App(__name__, specification_dir='swagger/', server='gevent')
    _app = connexion_app.app
    compose_yamls()
    #app.json_encoder = JSONEncoder
    _app.jinja_loader = FileSystemLoader(['server/templates'])

    _app.config.update(
            # CHANGE SECRET KEY AND SECURITY PASSWORD SALT!!!
            SECRET_KEY = "SHORTSTOPKEYTEST",
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(paths.db_path),
            SECURITY_PASSWORD_HASH = 'pbkdf2_sha512',
            SECURITY_TRACKABLE = False,
            SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production',
            SECURITY_POST_LOGIN_VIEW = '/',
            WTF_CSRF_ENABLED = False,
            STATIC_FOLDER=os.path.abspath('server/static')
        )

    _app.config["SECURITY_LOGIN_USER_TEMPLATE"] = "login_user.html"
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    connexion_app.add_api('composed_api.yaml')
    #_app.register_blueprint(app_page, url_prefix='/apps/<app>')
    return _app

# Template Loader
env = Environment(loader=FileSystemLoader("apps"))
app = create_app()


# Creates Test Data
@app.before_first_request
def create_user():
    from server.context import running_context
    from . import database

    running_context.db.create_all()

    if not database.User.query.first():
        admin_role = running_context.user_datastore.create_role(name='admin',
                                                                description='administrator',
                                                                pages=database.default_urls)

        u = running_context.user_datastore.create_user(email='admin', password=encrypt_password('admin'))
        running_context.user_datastore.add_role_to_user(u, admin_role)
        running_context.db.session.commit()

    apps = set(helpers.list_apps()) - set([_app.name
                                           for _app in running_context.db.session.query(running_context.App).all()])
    app.logger.debug('Found apps: {0}'.format(apps))
    for app_name in apps:
        running_context.db.session.add(running_context.App(app=app_name, devices=[]))
    running_context.db.session.commit()

    running_context.CaseSubscription.sync_to_subscriptions()

    app.logger.handlers = logging.getLogger('server').handlers


#@app_page.url_value_preprocessor
#def static_request_handler(endpoint, values):
#    g.app = values.pop('app', None)
#    app_page.static_folder = os.path.abspath(os.path.join('apps', g.app, 'interface', 'static'))