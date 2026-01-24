import copy
import functools
import re
from typing import cast
import yaml

from adam.config import Config
from adam.utils_k8s.ingresses import Ingresses

from . import __version__
from adam.utils_k8s.services import Services
from adam.utils import copy_config_file

class AppAction:
    def __init__(self, typ: str, name: str, payload: str = None, args: dict[str, str] = None, help: str = None):
        self.typ = typ
        self.name = name
        self.payload = payload
        self.args = args
        self.help = help

    def arguments(self):
        args = []

        if self.payload:
            i = 1
            while('{' + f'ARG{i}' + '}' in self.payload):
                args.append(f'ARG{i}')
                i += 1
        if self.args:
            for k, v in self.args.items():
                if k in args:
                    args = [v if x == k else x for x in args]

        return args

    def __str__(self):
        line = None

        args = ','.join(self.arguments())
        if args:
            line = f'{self.typ}.{self.name},{args}'
        else:
            line = f'{self.typ}.{self.name},'
        if self.help:
            line = f'{line},{self.help}'

        return line

class AppType:
    all_types: list['AppType'] = []

    def __init__(self, name: str, actions: list[AppAction], parents: list[str]):
        self.name = name
        self.actions = actions
        self.parents = parents

    def create(all_actions: dict) -> list['AppType']:
        if AppType.all_types:
            return AppType.all_types

        types = []

        for typ, actions in all_actions.items():
            parents = []

            groups = re.match(r'(.*?)\((.*)\)', typ)
            if groups:
                typ = groups[1]
                parents = groups[2].split(',')

            app_actions: list[AppAction] = []
            if actions:
                for action in actions:
                    for k, v in action.items():
                        aa: AppAction = None

                        if isinstance(v, str):
                            aa = AppAction(typ, k, help=v)
                        elif isinstance(v, dict):
                            args = {k: v1 for k, v1 in v.items()}
                            aa = AppAction(typ, k, payload=v['payload'], args=args, help=v['help'])
                        else:
                            aa = AppAction(typ, k)

                        app_actions.append(aa)

            types.append(AppType(typ, app_actions, parents=parents))

            AppType.all_types = types

        return types

    def app_type(all_actions: dict, name: str) -> 'AppType':
        if not AppType.all_types:
            AppType.all_types = AppType.create(all_actions)

        d = {t.name: t for t in AppType.all_types}
        if name in d:
            return d[name]

        return None

    def resolve_actions(all_actions: dict):
        if not AppType.all_types:
            AppType.all_types = AppType.create(all_actions)

        types = {t.name: t for t in AppType.all_types}

        def add_parents(typ: 'AppType', covered_parents: set[str] = set()):
            covered_parents.add(typ.name)

            for parent in typ.parents:
                typ.actions.extend(types[parent].actions)
                # break circular dependencies
                if not parent in covered_parents:
                    add_parents(types[parent], covered_parents=covered_parents)

        for typ in AppType.all_types:
            add_parents(typ)

        actions = {}
        for typ in AppType.all_types:
            for action in typ.actions:
                leaf = None

                if args := action.arguments():
                    for arg in reversed(args):
                        leaf = {arg: leaf}

                actions |= {f'{typ.name}.{action.name}': leaf}

        return actions

# utility collection on apps; methods are all static
class Apps:
    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Apps, cls).__new__(cls)

        return cls.instance

    def __init__(self, path: str = None):
        if path:
            try:
                with open(path) as f:
                    self.actions = cast(dict[str, any], yaml.safe_load(f))
            except:
                with open(copy_config_file(f'apps.yaml.{__version__}', 'adam.embedded_apps')) as f:
                    self.actions = cast(dict[str, any], yaml.safe_load(f))
        elif not hasattr(self, 'actions'):
            with open(copy_config_file(f'apps.yaml.{__version__}', 'adam.embedded_apps')) as f:
                self.actions = cast(dict[str, any], yaml.safe_load(f))

    def app_types(self) -> list[AppType]:
        return AppType.create(self.actions)

    @functools.lru_cache()
    def commands(self):
        return AppType.resolve_actions(self.actions)

    def payload(self, typ: str, action: str, args: list[str]) -> tuple[str, bool]:
        raw_args = ' '.join(args)

        app_type: AppType = AppType.app_type(self.actions, typ)
        if not app_type:
            return raw_args, True

        a0 = None
        p = None
        for a in app_type.actions:
            if a.name == action:
                a0 = a
                p = copy.copy(a.payload)
                break

        if not p:
            return raw_args, True

        if a0 and len(a0.arguments()) == 1:
            args = [' '.join(args)]

        for i, arg in enumerate(args):
            p = p.replace('{' + f'ARG{i+1}' + '}', arg)

        return p, 'ARG' not in p

    @functools.lru_cache()
    def envs() -> list[tuple[str, str]]:
        svcs = []

        for n, ns in Services.list_svc_name_and_ns(label_selector="applicationGroup=c3"):
            groups = re.match(r'.*?-(.*?)-(.*?)-.*', n)
            if groups:
                name = groups[1]

                if not (name, ns) in svcs:
                    svcs.append((name, ns))

        return svcs

    def find_namespace(env: str):
        for n, ns in Apps.envs():
            if n == env:
                return ns

        return None

    def app_host(env: str, app: str, namespace: str = None) -> str:
        if not namespace:
            namespace = Apps.find_namespace(env)

        ingress_name = Config().get('app.login.ingress', '{app_id}-k8singr-appleader-001').replace('{app_id}', f'{namespace}-{env}-{app}')

        return Ingresses.get_host(ingress_name, namespace)

    @functools.lru_cache()
    def apps(env: str) -> list[tuple[str, str]]:
        svcs = []

        for n, ns in Services.list_svc_name_and_ns(label_selector="applicationGroup=c3"):
            groups = re.match(r'.*?-(.*?)-(.*?)-.*', n)
            if groups and env == groups[1]:
                name = f'{groups[1]}-{groups[2]}'

                # {app_id}-k8singr-appleader-001
                # host = f"{Ingresses.get_host(f'{ns}-{groups[1]}-{groups[2]}-k8singr-appleader-001', ns)}"

                svcs.append((name, ns))

        return svcs