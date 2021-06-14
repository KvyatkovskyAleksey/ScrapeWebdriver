import os
import re
from zipfile import ZipFile
import shutil


def create_extension(username, password):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{path}/extension/background.js', 'w') as file:
        text = """
                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }
                
                browser.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
                );
               """ % (username, password)
        file.write(text)
    zip_file = ZipFile(f'{path}/extensions/extension.xpi', 'w')
    zip_file.write(f'{path}/extension/background.js', arcname='background.js')
    zip_file.write(f'{path}/extension/manifest.json', arcname='manifest.json')
    zip_file.close()


def create_anticaptcha_extension(api_key):
    path = os.path.dirname(os.path.realpath(__file__))
    with ZipFile(f'{path}/anticaptcha_plugin/anticaptcha-plugin_v0.56.xpi', 'r') as zip_file:
        zip_file.extractall(f'{path}/anticaptcha_plugin/anticaptcha-plugin')
    with open(f'{path}/anticaptcha_plugin/anticaptcha-plugin/js/config_ac_api_key.js') as file:
        js_text = ''.join(file.readlines())
    js_text = re.sub("antiCapthaPredefinedApiKey = ''", f"antiCapthaPredefinedApiKey = '{api_key}'", js_text)
    with open(f'{path}/anticaptcha_plugin/anticaptcha-plugin/js/config_ac_api_key.js', 'w') as file:
        file.write(js_text)
    shutil.make_archive(f'{path}/extensions/anticaptcha-plugin.xpi', 'zip',
                        f'{path}/anticaptcha_plugin/anticaptcha-plugin')
    os.rename(f'{path}/extensions/anticaptcha-plugin.xpi.zip',
              f'{path}/extensions/anticaptcha-plugin.xpi')
